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


def fibonacci_():
	x, y = 0, 1
	while True:
		yield x
		x, y = y, x+y

def tribonacci_():
	x, y, z = 0, 1, 1
	while True:
		yield x
		x, y, z = y, z, x+y+z
def lucas_():
	x, y = 2, 1
	while True:
		yield x
		x, y = y, x + y

def jacobsthal(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return jacobsthal(n-1) + 2 * jacobsthal(n - 2)

def pell(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return 2 * pell(n - 1) + pell(n - 2)

def perrin(n):
    if n == 0:
        return 3
    if n == 1:
        return 0
    if n == 2:
        return 2
    return perrin(n - 2) + perrin(n - 3)

def padovan(n):
    initial = [0, 1, 1]
    if n < len(initial):
        return initial[n]
    else:
        return padovan(n-2)+padovan(n-3)
