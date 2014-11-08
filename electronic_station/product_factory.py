from unittest import TestCase

def factors(n):
    for p in [2, 3, 5, 7]:
        while n % p == 0:
            yield p
            n /= p

def combis(factors):
    return [factors] + reduced

def possible_digits(f):
    return [f]

def checkio(N):
    return min("".join(d) for d in possible_digits(list(factors(N))))

"""
You are given a two or more digits number N. For this mission, you should find the smallest positive number of X,
such that the product of its digits is equal to N. If X does not exist, then return 0.

Let's examine the example. N = 20. We can factorize this number as 2*10, but 10 is not a digit. Also we can
factorize it as 4*5 or 2*2*5. The smallest number for 2*2*5 is 225, for 4*5 -- 45. So we select 45.

Hints: Remember prime numbers (numbers divisible by only one) and be careful with endless loops.

Input: A number N as an integer.

Output: The number X as an integer.
"""
class TestProductFactory(TestCase):
    def test_factors(self):
        self.assertEqual([2], list(factors(2)))
        self.assertEqual([2, 2], list(factors(4)))
        self.assertEqual([2, 2, 3], list(factors(12)))

    def test_combis(self):
        self.assertEqual([[2, 3], [6]], combis([2, 3]))

    def test_given(self):
        self.assertEqual(checkio(20), 45)
        self.assertEqual(checkio(21), 37)
        self.assertEqual(checkio(17), 0)
        self.assertEqual(checkio(33), 0)