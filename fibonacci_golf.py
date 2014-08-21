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

def construct(initial, coefficients):
    values = list(initial)
    while len(values) < 400:
        product = [a*b for a, b in zip(coefficients, values[::-1])]
        newvalue = sum(product)
        values.append(newvalue)

    return values


def fibgolf(type,num):
    function = construct(*({
        "fibonacci": ([0, 1], [1, 1]),
        "tribonacci": ([0, 1, 1], [1, 1, 1]),
        "lucas": ([2, 1], [1, 1]),
        "jacobsthal": ([0, 1], [1, 2]),
        "pell": ([0, 1], [1, 2]),
        "perrin": ([3, 0, 2], [0, 1, 1]),
        "padovan": ([0, 1, 1], [0, 1, 1])
    }[type]))
    return function[num]
