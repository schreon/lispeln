from lispeln.builtins import _plus
from lispeln.constants import Nil, Integer, Boolean
from lispeln.derived import Cons, Let, Begin
from lispeln.expressions import Symbol, Environment, Conditional, Procedure, Call, Define

__author__ = 'schreon'

import unittest


class DerivedTestCase(unittest.TestCase):
    """
    Test case for derived expressions.
    """
    def test_cons(self):
        a, b = Symbol("a"), Symbol("b")
        x = Cons(a, b)
        self.assertEquals(repr(x), "<Cons: ('a.'b)>")
        self.assertEquals(str(x), "('a . 'b)")
        self.assertIs(x.first, a)
        self.assertIs(x.rest, b)

        x = Cons(a, Cons(a, Cons(a, b)))
        self.assertEquals(x.ravel(), [a, a, a, b])
        self.assertEquals(str(x), "('a 'a 'a . 'b)")

        x = Cons(a, Cons(Cons(a, b), Cons(a, b)))
        self.assertEquals(str(x), "('a ('a . 'b) 'a . 'b)")

        x = Cons(a, Cons(b, Nil()))
        self.assertEquals(str(x), "('a 'b)")

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
