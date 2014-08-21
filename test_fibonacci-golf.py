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
        f = functions["fibonacci"]
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testTribonacci(self):
        f = functions["tribonacci"]
        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2)+f(n-3), "for n == "+str(n))

    def testLucas(self):
        f = functions["lucas"]
        f(0)==2, f(1)==1
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testJacobsthal(self):
        f = functions["jacobsthal"]
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+2*f(n-2), "for n == "+str(n))

    def testPadovan(self):
        f = functions["padovan"]
        self.assertEqual(0, f(0))
        self.assertEqual(1, f(1))
        self.assertEqual(1, f(2))

        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testPerrin(self):
        f = functions["perrin"]
        self.assertEqual(3, f(0))
        self.assertEqual(0, f(1))
        self.assertEqual(2, f(2))
        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testLengthOfCode(self):
        import local_checker
        self.assertLess(local_checker.check_file("fibonacci_golf.py"), 1709)

