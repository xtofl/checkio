from unittest import TestCase
from simplify import \
    Product as p, \
    Constant as c, \
    Power as x, \
    Sum as s, \
    simplify, \
    partition, partition_typed

__author__ = 'xtofl'


class TestProduct(TestCase):

    def test_Negative(self):
        self.assertEqual(True, p(c(-1), c(1)).negative())

    def test___factors(self):
        self.assertEqual(1, len(p([x(1)]).factors))
        self.assertSequenceEqual((x(1),), p(x(1)).factors)

    def test_PowerTerm(self):
        self.assertEqual(x(2), p(x(2)).power_factors())
        self.assertEqual(x(5), p(x(2), x(3)).power_factors())
        self.assertEqual(None, p(x(2), x(-2)).power_factors())

    def test_ConstantTerm(self):
        self.assertEqual(c(5), p(c(5)).constant_factor())
        self.assertEqual(c(15), p(c(5), c(3)).constant_factor())

    def test_Format(self):
        self.assertEqual("8*x**5", p(c(-8), x(5)).abs_fmt())
        self.assertEqual("8*x**5", p(c(8), x(5)).abs_fmt())


class TestSum(TestCase):

    def test_simplify_adds_equal_powers(self):
        self.assertEqual(s(p(c(2), x(1))), s(x(1), x(1)).simplify())

class TestSimplify(TestCase):

    def test_sum_factors(self):
        c1, c2, c3 = c(1), c(2), c(3)
        u, v = s(c1, c2), s(c2, c3)
        self.assertSequenceEqual((u, v), tuple(p(u, v).sum_factors()))
        self.assertSequenceEqual((u, v), tuple(p(u, v, c(1)).sum_factors()))

    def test_Format(self):
        self.assertEqual("1+2", s(c(1), c(2)).fmt())

        self.assertEqual("8*x**5", p(c(-8), x(5)).abs_fmt())
        self.assertEqual("8*x**5", p(c(8), x(5)).abs_fmt())

        term1 = p(c(8), x(5))
        term2 = p(c(-2), x(2))
        self.assertEqual("8*x**5-2*x**2", s(term1, term2).fmt())
        self.assertEqual(term1, term1)

    def test_ProductOfProducts(self):
        self.assertEqual(c(10), p(c(2), p(c(5))).simplify())
        self.assertEqual(c(10), p(p(c(5)), c(2)).simplify())

    def test_Distributivity_of_Multiplication(self):
        def eq(expect, original):
            self.assertEqual(expect, original.apply_distributivity())

        # x * 2 + x * 3 <-- x * (2 + 3)
        eq(s(
            p(x(1), c(2)),
            p(x(1), c(3))),
           p(x(1), s(c(2), c(3))))

        # 5 * (8x^5 - 2x^2) = 5*(8*x^5) + 5*(-2*x^2)
        term1 = p(c(8), x(5))
        term2 = p(c(-2), x(2))

        eq(s(p(c(5), p(c(8), x(5))),
             p(c(5), p(c(-2), x(2)))),
           p(c(5), s(term1, term2)))

    def test_sum_associativity(self):
        def eq(expect, original):
            self.assertEqual(set(expect.terms),
                             set(original.apply_associativity().terms))

        eq(s(1, 2, 3), s(1, s(2, 3)))
        eq(s(1, 2, 3), s(s(1, 2), 3))
        eq(s(1, 2, 3, 4), s(s(s(1, 2), 3), 4))

    def test_sum_distributivity(self):
        class X:
            def apply_distributivity(self):
                return s(1, 2, 3, 4)
        d = X()
        self.assertEqual(s(s(1, 2, 3, 4)), s(d).apply_distributivity())

    def after_associativity_test_Sum(self):
        class X:
            def __init__(self, simplified):
                self.simplified = simplified
            def simplify(self):
                return c(self.simplified)

        c1, c2, c3 = [c(i) for i in [1, 2, 3]]
        self.assertEqual(s(c1), s(X(1)).simplify())
        self.assertEqual(s(c1, c2, c3), s(X(1), X(2), X(3)).simplify())

        self.assertEqual(s(c1, c2), s(s(c1), s(c2)).simplify())

    def test_partition(self):
        odd = lambda x: x%2 == 1
        self.assertEqual([[], []], [list(p) for p in partition(odd, [])])
        self.assertEqual([[1], [0]], [list(p) for p in partition(odd, [0, 1])])

    def test_partition_typed(self):
        self.assertEqual([[], []], [list(p) for p in partition_typed(int, [])])
        self.assertEqual([[0], [1.0]], [list(p) for p in partition_typed(int, [0, 1.0])])


    def test_Product_Associativity(self):
        def eq(factors, expr):
            self.assertEqual(set(factors), set(expr.apply_associativity().factors))
        # 1 * (2 * 3) --> 1 * 2 * 3
        eq({1, 2, 3}, p(1, p(2, 3)))
        # (1 * 2 ) * 3 --> 1 * 2 * 3

        eq({1, 2, 3}, p(p(1, 2), 3))
        # (1 * (2 * (3 * 4))) --> 1 * 2 * 3 * 4
        self.assertEqual(p(1, 2, 3, 4), p(1, p(2, p(3, 4))).apply_associativity())

    def test_GivenExpressions(self):
        #"(x-1)*(x+1)"
        self.assertEqual("x**2-1", p(s(x(1), c(-1)), s(x(1), c(1))).simplify().fmt())
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))

    def _test_GivenStrings(self):
        self.assertEqual("x**2-1", simplify("(x-1)*(x+1)"))
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))