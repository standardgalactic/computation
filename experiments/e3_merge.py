"""E3: pathwise merge properties (Theorem pathmerge) on random trees."""
import random
random.seed(7)
BOT = None
def rand_tree(paths, base=None, change_p=0.2):
    t = {}
    for p in paths:
        if base is None: t[p] = random.choice([BOT, "a", "b", "c"])
        else: t[p] = base[p] if random.random() > change_p else random.choice([BOT, "a", "b", "c", "d"])
    return t
def D(t0, t): return {p for p in t0 if t[p] != t0[p]}
def merge(t0, t1, t2):
    d1, d2 = D(t0, t1), D(t0, t2)
    for p in d1 & d2:
        if t1[p] != t2[p]: return None
    return {p: (t1[p] if p in d1 else t2[p] if p in d2 else t0[p]) for p in t0}
paths = list(range(12)); N = 20000
sym = disj_def = assoc = cnt_assoc = undefined_conflict = overlap_trials = 0
bad = {"sym": 0, "disj_def": 0, "assoc": 0, "conflict": 0}
for _ in range(N):
    t0 = rand_tree(paths); t1 = rand_tree(paths, t0); t2 = rand_tree(paths, t0); t3 = rand_tree(paths, t0)
    a, b = merge(t0, t1, t2), merge(t0, t2, t1)
    if a != b: bad["sym"] += 1
    d1, d2, d3 = D(t0, t1), D(t0, t2), D(t0, t3)
    if not (d1 & d2):
        if a is None or D(t0, a) != d1 | d2: bad["disj_def"] += 1
    if not (d1 & d2) and not (d1 & d3) and not (d2 & d3):
        cnt_assoc += 1
        l = merge(t0, merge(t0, t1, t2), t3); r = merge(t0, t1, merge(t0, t2, t3))
        if l != r or l is None: bad["assoc"] += 1
    if any(t1[p] != t2[p] for p in d1 & d2):
        overlap_trials += 1
        if a is not None: bad["conflict"] += 1
print("trials", N, "disjoint_triples_checked", cnt_assoc, "conflicting_pairs", overlap_trials)
print("violations", bad)
