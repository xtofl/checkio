from unittest import TestCase
import itertools
from fibonacci_golf import *


class TestFib(TestCase):

    def testFibonacci(self):
        f = lambda n: fibgolf("fibonacci", n)
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testTribonacci(self):
        f = lambda n: fibgolf("tribonacci", n)
        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2)+f(n-3), "for n == "+str(n))

    def testLucas(self):
        f = lambda n: fibgolf("lucas", n)
        f(0)==2, f(1)==1
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testJacobsthal(self):
        f = lambda n: fibgolf("jacobsthal", n)
        self.assertEqual(0, f(0))
        self.assertEqual(1, f(1))
        for n in xrange(2, 400):
            self.assertEqual(f(n), f(n-1)+2*f(n-2), "for n == "+str(n))

    def testPadovan(self):
        f = lambda n: fibgolf("padovan", n)
        self.assertEqual(0, f(0))
        self.assertEqual(1, f(1))
        self.assertEqual(1, f(2))

        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testPerrin(self):
        f = lambda n: fibgolf("perrin", n)
        self.assertEqual(3, f(0))
        self.assertEqual(0, f(1))
        self.assertEqual(2, f(2))
        for n in xrange(3, 400):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testLengthOfCode(self):
        import local_checker
        self.assertLess(local_checker.check_file("fibonacci_golf.py"), 1078)

