# Series Repository Specification

**Working title:** *Learn to Reason About History* — companion repository specification
**Governing principles:**
1. Don't memorize Git. Learn to reason about history.
2. The repository is not the companion to the textbook. The repository is part of the textbook.

This document specifies the single companion Git repository shared across all seven volumes of the series. It is written before any volume's chapter outline, so that prose and repository grow together rather than the repository being manufactured after the fact to fit already-written exercises.

---

## 1. Repository Topology

### 1.1 One repository, one trunk
There is exactly one companion repository for the entire series, not one per volume. All seven running applications live inside it simultaneously:

```
repo/
    v1-webservice/          # Vol I — Dockerized personal web service
    v2-workstation/         # Vol II — Stable Diffusion workstation
    v3-research-assistant/  # Vol III — Ollama + Granite research assistant
    v4-essay-pipeline/      # Vol IV — essay-writing / LaTeX publishing pipeline
    v5-publishing-system/   # Vol V — collaborative publishing system
    v6-production-pipeline/ # Vol VI — connects v1–v5 into one pipeline
    v7-agent-repo/          # Vol VII — agent-maintained superset of the above
```

Each volume's application occupies its own top-level directory on the trunk. This is an assumption, stated explicitly so it can be overturned: the alternative (orphan branches per volume, merged nowhere) would keep histories cleaner in isolation but makes Volume VI's reconnection of the earlier projects a re-*telling* rather than a re-*use* of existing objects. Directory separation lets Volume VI reference `v2-workstation/` and `v3-research-assistant/` as they actually are on trunk, not as reintroduced copies.

Volumes remain **independently readable**: a reader starting at Volume IV clones the repository, checks out `v4/ch01/start`, and is inside `v4-essay-pipeline/` with everything needed for that volume already present at that ref. They are not required to have read Volumes I–III. The series is cumulative in concept, not a prerequisite chain in practice.

### 1.2 History is not sanitized
Failed approaches, abandoned branches, regressions, and ugly intermediate states are preserved deliberately. No force-pushes, no history rewrites, no squash-before-publish. A commit that represents a wrong turn is exactly as permanent as one that represents the fix.

---

## 2. The Immutable Tag Namespace

### 2.1 Tags are the textbook interface; branches are disposable
Annotated tags are the only permanent, citable coordinates in the repository. A textbook page can say "inspect `v4/ch11/broken`" and that reference is valid forever. Branches exist only as working surfaces students create locally from a tag and are free to destroy.

### 2.2 Tag vocabulary

```
v<volume>/ch<chapter>/start          # state at chapter open
v<volume>/ch<chapter>/checkpoint     # optional mid-chapter save point
v<volume>/ch<chapter>/ex<NN>/start   # state an individual exercise begins from
v<volume>/ch<chapter>/ex<NN>/solution # reference solution (see §5 on distribution)
```

Chapter-level `start`/`checkpoint` tags cover narrative continuity; exercise-level tags are the addressable unit for the manifest system (§4).

### 2.3 Working pattern
The book instructs students to detach or branch from a tag, never to work on trunk directly:

```
git switch --detach v4/ch11/broken
# or
git switch -c exercise/v4-ch11 v4/ch11/broken
```

Trunk (`main`) reflects the "current" state of each application as used by later volumes; it is not itself an exercise surface.

---

## 3. Preserved-but-Unreachable Objects

### 3.1 The problem
Some exercises require objects that are deliberately **not** reachable from any branch a student would casually merge into — an abandoned commit `I—J` off to the side, a dangling blob representing a deleted file, a commit that was later "lost" by a rewritten branch tip. Left as ordinary loose objects, these are legitimate targets for `git gc`.

### 3.2 Resolution: `refs/textbook/*` namespace
A dedicated ref namespace, outside `refs/heads/*` and `refs/tags/*`, holds pointers to every object the series requires to remain reachable without being part of any branch a student would encounter by default:

```
refs/textbook/v4/ch11/abandoned-I
refs/textbook/v4/ch11/abandoned-J
```

These refs are documented as permanently exempt from garbage collection. A student running plain `git gc` on their own clone may still prune what they don't have refs to locally — but the **published origin repository** retains these refs forever, so `git fetch` or a fresh clone always recovers the exercise's starting condition. The spec's rule: nothing under `refs/textbook/*` is ever deleted, renamed, or repointed.

### 3.3 Graph-shape exercises
Because these refs are ordinary Git refs, exercises can point directly at graph topology rather than file content:

```
D---E---F  experiment-a
                /
A---B---C-------G---H      main
        \
         I---J             refs/textbook/v4/ch11/abandoned-*
```

A chapter can ask: is `I` reachable from `main`? What is `mergebase(F, H)`? How would you transplant `E` onto `main` without bringing `F`? The repository functions as a figure printed alongside the prose — the manifest (§4) records which refs the question depends on.

---

## 4. Exercise Manifest

Every exercise carries a small machine-readable manifest, stored alongside the exercise (e.g. `v4-essay-pipeline/.textbook/ch11/ex03.yml`), decoupling the exercise definition from any particular grading platform.

### 4.1 Deterministic exercises
Machine-verifiable against a single expected artifact: an object ID, a tree, a recovered commit, a passing test suite.

```yaml
volume: 4
chapter: 11
exercise: 3
start: v4/ch11/ex03/start
verification: tree
expected: v4/ch11/ex03/solution
destructive: true
```

`destructive: true` flags exercises that instruct the student to rewrite history locally (e.g. practicing a disastrous rebase) — a signal to tooling that the student's branch, not trunk or any tag, is what gets modified.

### 4.2 Interpretive exercises
Introduced starting in Volume VII, where no single correct commit hash exists. These are evaluated against a stated rubric rather than an expected object:

```yaml
volume: 7
chapter: 8
exercise: 2
start: v7/ch08/ex02/start
verification: interpretive
rubric:
  - task-coherence
  - unrelated-change-isolation
  - recoverability
  - provenance
```

The rubric criteria are drawn from the acceptability model discussed for Volume VII:

$$
\text{acceptability} = f(\text{task relevance}, \text{semantic coherence}, \text{test evidence}, \text{provenance}, \text{reversibility})
$$

This is treated as a feature of the material, not a gap in the exercise design: Git can establish what happened without deciding what ought to survive, and Volume VII's exercises are where that distinction becomes the subject.

### 4.3 Verification types (extensible)
`tree`, `commit`, `object-id`, `reachability`, `tests-pass`, `interpretive`. New types can be added without changing the manifest schema, since `verification` is just a string field consumed by whatever runner a course adopts.

---

## 5. Solutions and Spoiler Isolation

**Open decision, resolved here as a default:** solution tags are *not* included in the default clone. A plain `git log --all` or `git tag -l` on a fresh clone must not reveal `v4/ch11/ex03/solution`.

Mechanism: solution-bearing refs live under a separate namespace (`refs/solutions/*`) hosted either as a second thin repository or as a remote configured with `fetch = +refs/solutions/*:refs/remotes/solutions/*` that the student adds explicitly once ready to check their work:

```
git remote add solutions <solutions-repo-url>
git fetch solutions
git diff exercise/v4-ch11 solutions/v4/ch11/ex03
```

This keeps the primary repository — the one students clone on day one — free of answers, while keeping the solution history itself version-controlled and citable the same way exercises are.

---

## 6. Release and Version Policy

- The companion repository is versioned independently of the books' print/PDF editions. A repository release tag (e.g. `series-v1.0`) marks the state of all `v<n>/...` tags at the time a given print edition went to press.
- **Published instructional history is never rewritten.** Once a chapter's tags are part of a release, the commits they point to are permanent. A discovered error is corrected by a new commit and, if necessary, a new tag (`v4/ch11/ex03/solution-v2`) — the original is never force-updated or deleted. This mirrors the series' own thesis: recoverability, not the illusion of a clean history, is the point.
- Deprecated tags (superseded by a `-v2`) remain resolvable indefinitely; they are marked deprecated in documentation, not removed.

---

## 7. Reset and Recovery Procedure

Because destructive exercises (§4.1) instruct students to damage their own local branch on purpose, the standard recovery path is documented once, centrally, rather than per-chapter:

```
git switch --detach <exercise-start-tag>
git branch -f exercise/<name> <exercise-start-tag>
git switch exercise/<name>
```

This discards any local damage and re-derives the working branch from the immutable tag. No student action can affect the origin repository's tags or `refs/textbook/*` namespace — those are read-only from the student's perspective by convention (enforced at the hosting level via branch/ref protection, not by anything Git itself guarantees).

---

## 8. Summary of Defaults Established Here

| Question | Default adopted |
|---|---|
| One repo or seven? | One repository, one trunk, one directory per volume's application |
| How do abandoned/unreachable objects survive? | `refs/textbook/*` namespace, permanent, GC-exempt |
| How are solutions kept from spoiling exercises? | Separate `refs/solutions/*` namespace / remote, fetched on demand |
| Can published history be rewritten? | Never — corrections are new commits/tags, originals stay resolvable |
| What is the addressable unit for tooling? | Exercise-level annotated tag + manifest file, not the whole repository |

Everything in this table is a stated assumption, not a constraint of Git itself, and can be revised before Volume I's chapter outline is built against actual repository state.

