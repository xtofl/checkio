from unittest import TestCase
from simplify import Product, Constant, Power, Sum, simplify, partition

__author__ = 'xtofl'


class TestSimplify(TestCase):

    def test_Product(self):
        self.assertEqual(True, Product(Constant(-1), Constant(1)).negative())

        self.assertEqual(1, len(Product(Power(1)).factors))
        self.assertSequenceEqual((Power(1),), Product(Power(1)).factors)

    def test_Product_PowerTerm(self):
        self.assertEqual(Power(2), Product(Power(2)).power_factors())
        self.assertEqual(Power(5), Product(Power(2), Power(3)).power_factors())
        self.assertEqual(None, Product(Power(2), Power(-2)).power_factors())

    def test_Product_ConstantTerm(self):
        self.assertEqual(Constant(5), Product(Constant(5)).constant_factor())
        self.assertEqual(Constant(15), Product(Constant(5), Constant(3)).constant_factor())

    def test_sum_factors(self):
        c1, c2, c3 = Constant(1), Constant(2), Constant(3)
        s, t = Sum(c1, c2), Sum(c2, c3)
        self.assertSequenceEqual((s, t), tuple(Product(s, t).sum_factors()))
        self.assertSequenceEqual((s, t), tuple(Product(s, t, Constant(1)).sum_factors()))

    def test_Format(self):
        self.assertEqual("1+2", Sum(Constant(1), Constant(2)).fmt())

        self.assertEqual("8*x**5", Product(Constant(-8), Power(5)).abs_fmt())
        self.assertEqual("8*x**5", Product(Constant(8), Power(5)).abs_fmt())

        term1 = Product(Constant(8), Power(5))
        term2 = Product(Constant(-2), Power(2))
        self.assertEqual("8*x**5-2*x**2", Sum(term1, term2).fmt())
        self.assertEqual(term1, term1)

    def test_ProductOfProducts(self):
        p = Product
        self.assertEqual(Constant(10), p(Constant(2), p(Constant(5))).simplify())
        self.assertEqual(Constant(10), p(p(Constant(5)), Constant(2)).simplify())

    def test_Distributivity(self):
        c = Constant
        p = Product
        s = Sum
        pw = Power
        # x * 2 + x * 3 <-- x * (2 + 3)
        self.assertEqual(Sum(p(pw(1), c(2)), p(pw(1), c(3))), p(pw(1), s(c(2), c(3))).apply_distributivity())

        # 5 * (8x^5 - 2x^2) = 40x^5 -10x^2
        term1 = Product(Constant(8), Power(5))
        term2 = Product(Constant(-2), Power(2))
        product = Product(Constant(5), Sum(term1, term2))
        self.assertEqual(s(p(c(5), p(c(8), pw(5))),
                           p(c(5), p(c(-2), pw(2)))), product.apply_distributivity())

    def test_Sum(self):
        class X:
            def __init__(self, simplified):
                self.simplified = simplified
            def simplify(self):
                return Constant(self.simplified)

        c1, c2, c3 = [Constant(i) for i in [1, 2, 3]]
        self.assertEqual(Sum(c1), Sum(X(1)).simplify())
        self.assertEqual(Sum(c1, c2, c3), Sum(X(1), X(2), X(3)).simplify())

        self.assertEqual(Sum(c1, c2), Sum(Sum(c1), Sum(c2)).simplify())

    def test_partition(self):
        odd = lambda x: x%2 == 1
        self.assertEqual([[], []], [list(p) for p in partition(odd, [])])
        self.assertEqual([[1], [0]], [list(p) for p in partition(odd, [0, 1])])

    def test_Product_Associativity(self):
        def eq(factors, expr):
            self.assertEqual(set(factors), set(expr.apply_associativity().factors))
        # 1 * (2 * 3) --> 1 * 2 * 3
        eq({1, 2, 3}, Product(1, Product(2, 3)))
        # (1 * 2 ) * 3 --> 1 * 2 * 3

        eq({1, 2, 3}, Product(Product(1, 2), 3))
        # (1 * (2 * (3 * 4))) --> 1 * 2 * 3 * 4
        self.assertEqual(Product(1, 2, 3, 4), Product(1, Product(2, Product(3, 4))).apply_associativity())

    def test_GivenExpressions(self):
        p = Product
        s = Sum
        c = Constant
        pw = Power
        #"(x-1)*(x+1)"
        self.assertEqual("x**2-1", p(s(pw(1), c(-1)), s(pw(1), c(1))).simplify().fmt())
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