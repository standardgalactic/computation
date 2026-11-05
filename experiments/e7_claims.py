"""E7: append-only claim log, replay, grounded labelling (Dung), prefix invariance, reinstatement, rule versioning."""
import random
random.seed(3)
def grounded(claims, attacks):
    # least fixed point of characteristic function; returns dict claim -> in/out/undec
    IN, OUT = set(), set()
    changed = True
    while changed:
        changed = False
        for c in claims:
            atk = [a for (a, b) in attacks if b == c]
            if c not in IN and all(a in OUT for a in atk): IN.add(c); changed = True
            if c not in OUT and any(a in IN for a in atk): OUT.add(c); changed = True
    return {c: ("in" if c in IN else "out" if c in OUT else "undec") for c in claims}
def naive(claims, attacks):  # a different "rule version": in iff unattacked by any live claim
    return {c: ("out" if any(b == c and a in claims for (a, b) in attacks) else "in") for c in claims}
def replay(log, rule=grounded):
    claims, attacks, retracted = set(), set(), set()
    for ev in log:
        if ev[0] == "claim": claims.add(ev[1])
        elif ev[0] == "attack": attacks.add((ev[1], ev[2]))
        elif ev[0] == "retract": retracted.add(ev[1])
    live = claims - retracted
    return rule(live, {(a, b) for (a, b) in attacks if a in live and b in live})
# reinstatement scenario a <- b <- c
log = [("claim", "a")]
snaps = [dict(replay(log))]
for ev in [("claim", "b"), ("attack", "b", "a"), ("claim", "c"), ("attack", "c", "b")]:
    log.append(ev); snaps.append(dict(replay(log)))
print("standing_of_a_over_time:", [s["a"] for s in snaps])
# prefix invariance on random logs
def rand_log(n):
    L, ids = [], []
    for _ in range(n):
        r = random.random()
        if r < 0.45 or len(ids) < 2: i = f"n{len(ids)}"; ids.append(i); L.append(("claim", i))
        elif r < 0.9: L.append(("attack", random.choice(ids), random.choice(ids)))
        else: L.append(("retract", random.choice(ids)))
    return L
viol_prefix = viol_iso = diff_rule = total = nonmono = 0
for _ in range(2000):
    L = rand_log(25); snap = []
    for k in range(1, len(L) + 1): snap.append(replay(L[:k]))
    # recompute after "appending later events": prefix replays must be unchanged
    for k in range(1, len(L) + 1):
        if replay(L[:k]) != snap[k - 1]: viol_prefix += 1
    st = replay(L)
    # isomorphism invariance: rename ids
    ids = sorted({x for ev in L for x in ev[1:]}); perm = dict(zip(ids, random.sample(ids, len(ids))))
    L2 = [(ev[0],) + tuple(perm[x] for x in ev[1:]) for ev in L]
    st2 = replay(L2)
    if {perm[c]: v for c, v in st.items()} != st2: viol_iso += 1
    if replay(L, grounded) != replay(L, naive): diff_rule += 1
    # non-monotonic standing: some claim changes in->out->in across the log
    for c in st:
        seq = [s.get(c) for s in snap if c in s]
        flips = sum(1 for x, y in zip(seq, seq[1:]) if x != y)
        if flips >= 2: nonmono += 1; break
    total += 1
print("logs", total, "prefix_violations", viol_prefix, "isomorphism_violations", viol_iso)
print("logs_where_rule_versions_disagree", diff_rule, "logs_with_reinstatement_flips", nonmono)
