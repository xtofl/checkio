from unittest import TestCase
import itertools
from fibonacci_golf import *

def itake(n, sequence):
    for x in sequence:
        if n == 0:
            return
        yield x
        n -= 1

def take(n, sequence):
    return list(itake(n, sequence))

def takef(n, iterable):
    sequence = take(n, iterable)
    def f(n):
        return sequence[n]
    return f

class TestFib(TestCase):

    def testTake(self):
        f = takef(20, xrange(20))
        self.assertEqual(10, f(10))

    def testFibonacci(self):
        f = takef(20, fibonacci_())
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testTribonacci(self):
        f = takef(20, tribonacci_())
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2)+f(n-3), "for n == "+str(n))

    def testLucas(self):
        f = takef(20, lucas_())
        f(0)==2, f(1)==1
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+f(n-2), "for n == "+str(n))

    def testJacobsthal(self):
        f = takef(20, itertools.imap(lambda n: jacobsthal(n), itertools.count()))
        for n in xrange(2, 10):
            self.assertEqual(f(n), f(n-1)+2*f(n-2), "for n == "+str(n))

    def testPerrin(self):
        f = takef(20, itertools.imap(lambda n: perrin(n), itertools.count()))
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

    def testPadovan(self):
        f = takef(20, itertools.imap(lambda n: padovan(n), itertools.count()))
        for n in xrange(3, 10):
            self.assertEqual(f(n), f(n-2)+f(n-3), "for n == "+str(n))

