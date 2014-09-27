from itertools import product, chain
from operator import mul, add
from functools import reduce
from Onboard.pypredict.lm_wrapper import filter_tokens

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


def filter_type(t, it):
    return (i for i in it if type(it) is t)

def filter_type_not(t, it):
    return (i for i in it if not type(it) is t)


class Sum(Expr):
    def __init__(self, *terms):
        self.terms = tuple(terms)

    def fmt(self):
        return self.terms[0].abs_fmt() + \
               "".join([
                   ('-' if t.negative() else '+') + t.abs_fmt()
                   for t in self.terms[1:]])

    def simplify(self):
        simplified_terms = [t.simplify() for t in self.terms]

        sum_terms = reduce(lambda l, t: l + t,
                           list(t.terms for t in filter_type(Sum, simplified_terms)),
                           list())
        other_terms = list(filter_type_not(Sum, simplified_terms))
        return Sum(*(sum_terms + other_terms))

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

def partition(predicate, it):
    ins, outs = [], []
    for i in it:
        (ins if predicate(i) else outs).append(i)

    return (ins, outs)

class Product(Expr):
    def __init__(self, *factors):
        self.factors = tuple(factors)

    def negative(self):
        return sum((f.negative() for f in self.factors)) % 2 == 1

    def power_factors(self):
        powers = tuple(filter_type(Power, self.factors))
        exponent = reduce(add, (p.exponent for p in powers), 0)
        return Power(exponent) if exponent else None

    def constant_factor(self):
        constants = (f for f in self.factors if type(f) is Constant)
        constant = Constant(reduce(mul, (c.value for c in constants), 1)) if constants else None
        return constant

    def sum_factors(self):
        return (f for f in self.factors if type(f) is Sum)

    def apply_associativity(self):
        products, simple_factors = partition(lambda f: type(f) is Product, self.factors)
        extra_factors = chain(*(p.factors for p in products))
        return Product(*chain(simple_factors, extra_factors))

    def simplify(self):

        simplified_products = (f.simplify() for f in self.factors if type(f) is Product)

        constant = self.constant_factor()
        constant = reduce(mul, (c.value for c in simplified_products if type(c) is Constant), constant.value)

        powers = self.power_factors()

        sums = list(chain(self.sum_factors(), (s for s in simplified_products if type(s) is Sum)))
        simple_factors = [f for f in (Constant(constant), self.power_factors()) if f]
        if not sums:
            if not powers:
                return Constant(constant)
            return Product(*simple_factors)
        else:
            terms_combined = product(*[s.terms for s in sums])
            combis = [Product(
                        *list(
                            chain(simple_factors, c)))
                      for c in terms_combined]
            return Sum(*combis).simplify()

    def simple_factors(self):
        return tuple(f for f in (self.constant_factor(), self.power_factors()) if f)

    def distribute(self, terms):
        return Sum(*[Product(*(self.simple_factors() + (t,))) for t in terms])

    def abs_fmt(self):
        return "*".join((f.abs_fmt() for f in self.factors))

    def __repr__(self):
        return "Product({})".format(", ".join(repr(f) for f in self.factors))

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


