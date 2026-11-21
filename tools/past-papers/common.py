"""Helpers shared by the past paper series files."""
import sympy as sp

x, y, t, k, r, theta, h, u, n = sp.symbols("x y t k r theta h u n", real=True)


def card(paper, q, front, back, choices, ask=None):
    c = {"paper": paper, "q": q, "front": front, "back": back, "choices": choices}
    if ask:
        c["ask"] = ask
    return c


def close(a, b, tol=1e-9):
    """True when two numbers agree to a relative tolerance."""
    a, b = float(a), float(b)
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def same(a, b):
    """True when two sympy expressions are identical."""
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


def identity(expr, var, lo=0.1, hi=1.4, n=25):
    """True when expr is zero at n points of (lo, hi) (for identities sympy can't simplify)."""
    f = sp.lambdify(var, expr, "math")
    for i in range(n):
        v = lo + (hi - lo) * (i + 0.5) / n
        if abs(f(v)) > 1e-9:
            return False
    return True
