"""E4: dependency resolution depends on registry time; pinning by hash does not."""
import hashlib, json
def h(name, ver): return hashlib.sha256(f"{name}=={ver}".encode()).hexdigest()[:12]
registry_t0 = {"libx": ["1.0", "1.1"], "liby": ["2.0"]}
registry_t1 = {"libx": ["1.0", "1.1", "1.2", "2.0"], "liby": ["2.0", "2.1"]}
req = {"libx": (">=1.0", "<2.0"), "liby": (">=2.0", None)}
def key(v): return tuple(int(x) for x in v.split("."))
def resolve(reg):
    out = {}
    for n, (lo, hi) in req.items():
        lo_v = key(lo[2:]); hi_v = key(hi[1:]) if hi else None
        ok = [v for v in reg[n] if key(v) >= lo_v and (hi_v is None or key(v) < hi_v)]
        out[n] = max(ok, key=key)
    return out
r0, r1 = resolve(registry_t0), resolve(registry_t1)
print("resolved_t0:", r0); print("resolved_t1:", r1); print("differs_over_time:", r0 != r1)
lock = {n: (v, h(n, v)) for n, v in r0.items()}
def resolve_pinned(reg, lock):
    out = {}
    for n, (v, hh) in lock.items():
        out[n] = v if v in reg[n] and h(n, v) == hh else None
    return out
print("pinned_t0:", resolve_pinned(registry_t0, lock)); print("pinned_t1:", resolve_pinned(registry_t1, lock))
print("pinned_invariant:", resolve_pinned(registry_t0, lock) == resolve_pinned(registry_t1, lock))
