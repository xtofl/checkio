from unittest import TestCase
from simplify import Product, Constant, Power, Sum, simplify

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
        prod = p(c(1))
        self.assertEqual(Sum(p(c(1), c(2)), p(c(1), c(3))), p(c(1)).distribute((c(2), c(3))))

        term1 = Product(Constant(8), Power(5))
        term2 = Product(Constant(-2), Power(2))
        s = Sum(term1, term2)
        factor = Constant(5)
        product = Product(Constant(5), s) # 5 * (8x^5 - 2x^2) = 40x^5 -10x^2
        simplified = product.simplify()
        self.longMessage = True
        self.assertEqual(str(Sum(Product(Constant(40), Power(5)), Product(Constant(-10), Power(2)))),
                         str(simplified))

    def _test_Given(self):
        self.assertEqual("x**2-1", simplify("(x-1)*(x+1)"))
        self.assertEqual("x**2+2*x+1", simplify("(x+1)*(x+1)"))
        self.assertEqual("x**2+6*x", simplify("(x+3)*x*2-x*x"))
        self.assertEqual("x**3+x**2+x", simplify("x+x*x+x*x*x"))
        self.assertEqual("x**4+3*x+6", simplify("(2*x+3)*2-x+x*x*x*x"))
        self.assertEqual("0", simplify("x*x-(x-1)*(x+1)-1"))
        self.assertEqual( "-x", simplify("5-5-x"))
        self.assertEqual("-1", simplify("x*x*x-x*x*x-1"))