from lispeln.constants import Nil
from lispeln.derived import Cons
from lispeln.expressions import Symbol

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

if __name__ == '__main__':
    unittest.main()
