"""E1: lineage invariants under clone, relocation, rebase, cherry-pick (real git)."""
import subprocess, tempfile, os, json, sys

def g(args, cwd, env=None):
    e = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="t",
             GIT_COMMITTER_EMAIL="t@x", GIT_AUTHOR_DATE="2026-01-01T00:00:00", GIT_COMMITTER_DATE="2026-01-01T00:00:00")
    if env: e.update(env)
    return subprocess.run(["git"] + args, cwd=cwd, env=e, capture_output=True, text=True, check=True).stdout.strip()

def patch_id(commit, cwd):
    p = subprocess.run(f"git show {commit} | git patch-id --stable", shell=True, cwd=cwd, capture_output=True, text=True)
    return p.stdout.split()[0]

def run(k):
    d = tempfile.mkdtemp(prefix="e1_")
    r = os.path.join(d, "src"); os.makedirs(r)
    g(["init", "-q", "-b", "main"], r)
    def commit(fname, text, msg):
        open(os.path.join(r, fname), "w").write(text); g(["add", fname], r); g(["commit", "-q", "-m", msg], r)
        return g(["rev-parse", "HEAD"], r)
    base = commit("base.txt", "base\n", "base")
    g(["checkout", "-q", "-b", "feature"], r)
    seg = [commit(f"f{i}.txt", f"feature {i}\n", f"f{i}") for i in range(k)]
    g(["checkout", "-q", "main"], r)
    newbase = commit("main2.txt", "main change\n", "main2")
    # clone: ids preserved?
    c = os.path.join(d, "clone"); g(["clone", "-q", "--mirror", r, c], d)
    cl_ids = set(g(["rev-list", "--all"], c).split())
    src_ids = set(g(["rev-list", "--all"], r).split())
    clone_ok = cl_ids == src_ids
    # rebase feature onto main
    g(["checkout", "-q", "feature"], r)
    g(["rebase", "-q", "main"], r)
    new = g(["rev-list", "--reverse", f"main..feature"], r).split()
    ids_differ = all(a != b for a, b in zip(seg, new))
    patch_eq = all(patch_id(a, r) == patch_id(b, r) for a, b in zip(seg, new))
    order_ok = all(subprocess.run(["git", "merge-base", "--is-ancestor", new[i], new[j]], cwd=r).returncode == 0
                   for i in range(k) for j in range(i + 1, k))
    old_not_anc = all(subprocess.run(["git", "merge-base", "--is-ancestor", o, n], cwd=r).returncode != 0 for o in seg for n in new)
    # cherry-pick of the first old commit onto main
    g(["checkout", "-q", "-b", "cp", "main"], r)
    g(["cherry-pick", seg[0]], r)
    cp = g(["rev-parse", "HEAD"], r)
    cp_ok = (cp != seg[0]) and patch_id(cp, r) == patch_id(seg[0], r)
    return dict(k=k, clone_ids_preserved=clone_ok, rebased_ids_differ=ids_differ, patch_equiv=patch_eq,
                order_preserved=order_ok, old_not_ancestors=old_not_anc, cherrypick_new_id_same_patch=cp_ok)

if __name__ == "__main__":
    res = [run(k) for k in (2, 3, 5, 8, 13)]
    for x in res: print(json.dumps(x))
    ok = all(all(v for kk, v in x.items() if kk != "k") for x in res)
    print("ALL_PROPERTIES_HOLD:", ok)
