"""
fibonacci:
f(0)=0, f(1)=1, f(n)=f(n-1)+f(n-2)
tribonacci:
f(0)=0, f(1)=1, f(2)=1, f(n)=f(n-1)+f(n-2)+f(n-3)
lucas:
f(0)=2, f(1)=1, f(n)=f(n-1)+f(n-2)
jacobsthal:
f(0)=0, f(1)=1, f(n)=f(n-1)+2*f(n-2)
pell:
f(0)=0, f(1)=1, f(n)=2*f(n-1)+f(n-2)
perrin:
f(0)=3, f(1)=0, f(2)=2, f(n)=f(n-2)+f(n-3)
padovan:
f(0)=0, f(1)=1, f(2)=1, f(n)=f(n-2)+f(n-3)
"""

def construct(initial, recursive):
    def f(n):
        if n < len(initial): return initial[n]
        return recursive(f, n)
    return f

functions = {
    "fibonacci": construct([0, 1], lambda f, n: f(n-1)+f(n-2)),
    "tribonacci": construct([0, 1, 1], lambda f, n: f(n-1)+f(n-2)+f(n-3)),
    "lucas": construct([2, 1], lambda f, n: f(n-1)+f(n-2)),
    "jacobsthal": construct([0, 1], lambda f, n: f(n-1) + 2 * f(n-2)),
    "pell": construct([0, 1], lambda f, n: 2 * f(n-1) + f(n-2)),
    "padovan": construct([0, 1, 1], (lambda f, n: f(n-2) + f(n-3))),
    "perrin": construct([0, 1, 2], lambda f, n: f(n-2) + f(n-3))
}