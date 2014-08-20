from unittest import TestCase
import itertools
from fibonacci_golf import *

def takef(n, f):
    sequence = map(f, xrange(n))
    def f(n):
        return sequence[n]
    return f

class TestFib(TestCase):

    def testFibonacci(self):
        f = takef(20, fibonacci)
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testTribonacci(self):
        f = tribonacci
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2)+f(n-3), "for n == "+str(n))

    def testLucas(self):
        f = lucas
        f(0)==2, f(1)==1
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testJacobsthal(self):
        f = jacobsthal
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+2*f(n-2), "for n == "+str(n))

    def testPerrin(self):
        f = perrin
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testPadovan(self):
        f = padovan
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

