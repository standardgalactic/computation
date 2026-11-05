"""E8: extraction and hoisting preserve expansion; hoisting without side conditions can fail."""
import random, copy
random.seed(5)
# terms: ("atom", s) | ("ref", n) | ("node", [children]) | ("let", n, d, body)
def rand_term(depth, names):
    r = random.random()
    if depth == 0 or r < 0.2:
        return ("ref", random.choice(names)) if names and random.random() < 0.4 else ("atom", random.choice("abc"))
    if r < 0.65: return ("node", [rand_term(depth - 1, names) for _ in range(random.randint(1, 3))])
    n = random.choice("xyz"); d = rand_term(depth - 1, names)
    return ("let", n, d, rand_term(depth - 1, names + [n]))
def expand(t, env):
    k = t[0]
    if k == "atom": return t
    if k == "ref": return expand(env[t[1]][0], env[t[1]][1]) if t[1] in env else ("unbound", t[1])
    if k == "node": return ("node", [expand(c, env) for c in t[1]])
    if k == "let":
        e2 = dict(env); e2[t[1]] = (t[2], env)   # lexical: definition sees env at its let
        return expand(t[3], e2)
def fv(t, bound=frozenset()):
    k = t[0]
    if k == "atom": return set()
    if k == "ref": return set() if t[1] in bound else {t[1]}
    if k == "node": return set().union(*[fv(c, bound) for c in t[1]])
    return fv(t[2], bound) | fv(t[3], bound | {t[1]})
def subterms(t):
    yield t
    if t[0] == "node":
        for c in t[1]: yield from subterms(c)
    if t[0] == "let": yield from subterms(t[2]); yield from subterms(t[3])
def replace(t, s, ref):
    if t == s: return ref
    if t[0] == "node": return ("node", [replace(c, s, ref) for c in t[1]])
    if t[0] == "let": return ("let", t[1], replace(t[2], s, ref), replace(t[3], s, ref))
    return t
def extract(t):
    # closed repeated node subterm (no free refs) -> let fresh = s in t[s := ref fresh]
    cands = [s for s in subterms(t) if s[0] == "node" and not fv(s)]
    for s in cands:
        if sum(1 for u in subterms(t) if u == s) >= 2:
            return ("let", "w", s, replace(t, s, ("ref", "w")))
    return None
def hoist(t):
    # let x = d1 in (let y = d2 in b)  ->  let y = d2 in (let x = d1 in b)
    if t[0] == "let" and t[3][0] == "let": return ("let", t[3][1], t[3][2], ("let", t[1], t[2], t[3][3]))
    return None
def side_ok(t): x, d1, y, d2 = t[1], t[2], t[3][1], t[3][2]; return x != y and y not in fv(d1) and x not in fv(d2)
stats = dict(extract_tried=0, extract_ok=0, hoist_ok_cond=0, hoist_ok_cond_pres=0, hoist_viol=0, hoist_viol_changed=0)
for _ in range(30000):
    t = rand_term(5, [])
    if "w" in {n for u in subterms(t) if u[0] == "let" for n in [u[1]]} | fv(t): continue
    e = extract(t)
    if e is not None:
        stats["extract_tried"] += 1; stats["extract_ok"] += expand(t, {}) == expand(e, {})
    h = hoist(t)
    if h is not None:
        # restrict to terms whose own free refs are none (closed) to avoid unbound artefacts
        if fv(t): continue
        if side_ok(t): stats["hoist_ok_cond"] += 1; stats["hoist_ok_cond_pres"] += expand(t, {}) == expand(h, {})
        else: stats["hoist_viol"] += 1; stats["hoist_viol_changed"] += expand(t, {}) != expand(h, {})
print(stats)
