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

def construct(args):
    name, initial, recursive = args
    cache = dict(enumerate(initial))
    def f(n):
        if n in cache: return cache[n]
        cache[n] = recursive(f, n)
        return cache[n]
    return name, f

functions = dict(map(construct, [
    ("fibonacci", [0, 1], lambda f, n: f(n-1)+f(n-2)),
    ("tribonacci", [0, 1, 1], lambda f, n: f(n-1)+f(n-2)+f(n-3)),
    ("lucas", [2, 1], lambda f, n: f(n-1)+f(n-2)),
    ("jacobsthal", [0, 1], lambda f, n: f(n-1) + 2 * f(n-2)),
    ("pell", [0, 1], lambda f, n: 2 * f(n-1) + f(n-2)),
    ("padovan", [0, 1, 1], lambda f, n: f(n-2) + f(n-3)),
    ("perrin", [0, 1, 2], lambda f, n: f(n-2) + f(n-3))
    ]))


def fibgolf(type,num):
    return functions[type](num)
