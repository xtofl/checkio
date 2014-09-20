from itertools import product, chain
from operator import mul, add
from functools import reduce

__mission__ = """http://www.checkio.org/mission/simplification/share/cd052a5416a6e8b459e74b63451b9c30/"""


class Expr:
    def __repr__(self):
        return self.abs_fmt()


class Constant(Expr):
    def __init__(self, value):
        self.value = value

    def negative(self):
        return self.value < 0

    def abs_fmt(self):
        return str(abs(self.value))

    def simplify(self):
        return self

    def __eq__(self, other):
        if not type(other) is Constant:
            return False
        return self.value == other.value


class Power(Expr):
    def __init__(self, exponent):
        self.exponent = exponent

    def abs_fmt(self):
        return "x**{}".format(self.exponent)

    def negative(self):
        return False

    def simplify(self):
        return self

    def __eq__(self, other):
        if not type(other) is Power:
            return False
        return self.exponent == other.exponent


class Sum(Expr):
    def __init__(self, *terms):
        self.terms = tuple(terms)

    def fmt(self):
        return self.terms[0].abs_fmt() + \
               "".join([
                   ('-' if t.negative() else '+') + t.abs_fmt()
                   for t in self.terms[1:]])

    def simplify(self):
        return reduce(lambda lst, t: lst+(t,), (t.simplify() for t in self.terms))

    def abs_fmt(self):
        return "+".join((f.abs_fmt() for f in self.terms))

    def __repr__(self):
        return "Sum({})".format(tuple(repr(t) for t in self.terms))

    def __eq__(self, other):
        if self is other:
            return True
        if not type(other) is Sum:
            return False
        return self.terms == other.terms


class Product(Expr):
    def __init__(self, *factors):
        self.factors = tuple(factors)

    def negative(self):
        return sum((f.negative() for f in self.factors)) % 2 == 1

    def power_factors(self):
        powers = tuple(f for f in self.factors if type(f) is Power)
        exponent = reduce(add, (p.exponent for p in powers), 0)
        return Power(exponent)

    def constant_factor(self):
        constants = (f for f in self.factors if type(f) is Constant)
        constant = Constant(reduce(mul, (c.value for c in constants), 1)) if constants else None
        return constant

    def sum_factors(self):
        return (f for f in self.factors if type(f) is Sum)

    def simplify(self):
        constant = self.constant_factor()

        simple_factors = (f for f in (constant, self.power_factors()) if f)

        sums = self.sum_factors()
        if not sums:
            return Product(simple_factors)
        else:
            distributed = (Product(*chain(simple_factors, c)) for c in product(sums))
            return Sum(*distributed)

    def abs_fmt(self):
        return "*".join((f.abs_fmt() for f in self.factors))

    def __repr__(self):
        return "Product({})".format(tuple(repr(f) for f in self.factors))

    def __eq__(self, other):
        if other is self:
            return True
        if not type(other) is Product:
            return False
        return self.factors == other.factors


def parse(expr):
    """returns an expression tree"""
    return Sum(Power(2), Constant(-1))


def simplify(expr):
    return str(parse(expr))


class Reductions:

    @staticmethod
    def distribute(factor, terms):
        return tuple((t, factor) for t in terms)


