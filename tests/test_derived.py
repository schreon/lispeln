from lispeln.builtins import plus
from lispeln.constants import Nil, Integer, Boolean
from lispeln.derived import Cons, Let
from lispeln.expressions import Symbol, Environment, Conditional, Procedure, Call

__author__ = 'schreon'

import unittest


class DerivedTestCase(unittest.TestCase):

    def test_cons(self):
        a, b = Symbol("a"), Symbol("b")
        x = Cons(a, b)
        self.assertEquals(repr(x), "<Cons: ('a.'b)>")
        self.assertEquals(str(x), "('a . 'b)")
        self.assertEquals(x.first, a)
        self.assertEquals(x.rest, b)

        x = Cons(a, Cons(a, Cons(a, b)))
        self.assertEquals(x.ravel(), [a, a, a, b])
        self.assertEquals(str(x), "('a 'a 'a . 'b)")

        x = Cons(a, Cons(Cons(a, b), Cons(a, b)))
        self.assertEquals(str(x), "('a ('a . 'b) 'a . 'b)")

        x = Cons(a, Cons(b, Nil()))
        self.assertEquals(str(x), "('a 'b)")

    def test_let(self):
        env = Environment(None)
        env['+'] = Procedure(plus)
        env['x'] = Integer(0)
        env['y'] = Integer(1)

        let = Let([(Symbol('x'), Integer(10))], Call(Symbol('+'), Symbol('x'), Symbol('y')))

        self.assertEquals(let.eval(env), Integer(11))

if __name__ == '__main__':
    unittest.main()
