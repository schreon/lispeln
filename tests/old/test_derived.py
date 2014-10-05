from lispeln.scheme.assignment import Define
from lispeln.evaluator.builtins import _plus
from lispeln.scheme.constants import Nil, Integer
from lispeln.scheme.derived import Pair, Let, Begin
from lispeln.evaluator.environment import Environment
from lispeln.scheme.procedure import Procedure, Call
from lispeln.scheme.symbol import Symbol

__author__ = 'schreon'

import unittest


class DerivedTestCase(unittest.TestCase):
    """
    Test case for derived expressions.
    """
    def test_cons(self):
        a, b = Symbol("a"), Symbol("b")
        x = Pair(a, b)
        self.assertIs(x.first, a)
        self.assertIs(x.rest, b)

        env = Environment(None)
        env['a'] = Integer(123)
        env['b'] = Integer(42)

        x = Pair(a, Pair(a, Pair(a, Pair(b, Nil()))))
        e = x.eval(env)
        self.assertEquals(e.first, Integer(123))
        self.assertEquals(e.rest.rest.rest.first, Integer(42))


    def test_let(self):
        env = Environment(None)
        env['+'] = Procedure(_plus)
        env['y'] = Integer(1)

        let = Let([(Symbol('x'), Integer(10))], Call(Symbol('+'), Symbol('x'), Symbol('y')))

        self.assertEquals(let.eval(env), Integer(11))
        self.assertNotIn(Symbol('x'), env)

    def test_begin(self):
        env = Environment(None)

        begin = Begin(
            Define(Symbol('a'), Integer(42)),
            Define(Symbol('b'), Integer(-42)),
            Call(Procedure(_plus), Symbol('a'), Symbol('b'))
        )

        self.assertEquals(begin.eval(env), Integer(0))

if __name__ == '__main__':
    unittest.main()
