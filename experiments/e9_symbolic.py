"""E9: symbolic derivations and declared assumptions (requires sympy)."""
import random, sympy as sp
x, a, b, c, d = sp.symbols('x a b c d')
xr = sp.Symbol('xr', real=True); xp = sp.Symbol('xp', positive=True)
print("sympy", sp.__version__)
# 1. the simplification of sqrt(x^2) depends on the declared assumptions
for name, s in [("no assumption", x), ("real", xr), ("positive", xp)]:
    print("sqrt(s^2) with", name, "->", sp.simplify(sp.sqrt(s**2)))
# 2. cancellation changes the domain
e0 = (x**2 - 1)/(x - 1); e1 = sp.cancel(e0)
print("cancel ->", e1, "; value of original at 1:", e0.subs(x, 1), "; value of result at 1:", e1.subs(x, 1))
# 3. squaring introduces an extraneous solution
cands = sp.solve(sp.Eq(x + 2, x**2), x)
valid = [r for r in cands if sp.simplify(sp.sqrt(r + 2) - r) == 0]
print("candidates after squaring:", cands, "; satisfying sqrt(x+2)=x:", valid)
# 4. Lotka-Volterra Jacobian at the interior equilibrium
X, Y = sp.symbols('X Y')
f = sp.Matrix([a*X - b*X*Y, c*X*Y - d*Y])
J = f.jacobian([X, Y]).subs({X: d/c, Y: a/b})
J = sp.simplify(J)
ev = list(J.eigenvals().keys())
print("Jacobian:", J.tolist(), "; eigenvalues:", ev)
# 5. numerical substitution audit of the identity under the declared domain x != 1
random.seed(0); bad = 0; tested = 0
for _ in range(1000):
    v = sp.Rational(random.randint(-50, 50), random.randint(1, 9))
    if v == 1: continue
    tested += 1
    if e0.subs(x, v) != e1.subs(x, v): bad += 1
print("substitution audit on x != 1: tested", tested, "failures", bad)
