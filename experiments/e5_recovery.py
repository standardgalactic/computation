"""E5: Monte Carlo check of the two-channel recovery model R = 1-(1-exp(-lam*D))(1-s)."""
import random, math
random.seed(11)
def mc(lam, s, D, n=200000):
    ok = 0
    for _ in range(n):
        mem = random.random() < math.exp(-lam * D); rec = random.random() < s
        ok += (mem or rec)
    return ok / n
print("lam s D empirical analytic abs_err")
mx = 0
for lam in (0.1, 0.5, 1.0):
    for s in (0.0, 0.3, 0.7):
        for D in (0.0, 1.0, 5.0, 20.0):
            e = mc(lam, s, D); a = 1 - (1 - math.exp(-lam * D)) * (1 - s); mx = max(mx, abs(e - a))
            print(lam, s, D, round(e, 4), round(a, 4), round(abs(e - a), 4))
print("max_abs_error", round(mx, 4))
