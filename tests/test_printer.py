from lispeln.printer.derived import print_cons, print_expression
from lispeln.scheme.constants import Nil, Integer
from lispeln.scheme.derived import Cons
from lispeln.scheme.expressions import Symbol, Environment

__author__ = 'schreon'

import unittest

import logging

logging.basicConfig(level=logging.INFO)

class PrinterTestCase(unittest.TestCase):
    def test_cons(self):

        env = Environment(None)
        env['a'] = Integer(123)
        env['b'] = Integer(42)

        s = print_expression(Cons(Symbol('a'), Symbol('b')).eval(env))
        self.assertEquals("(123 . 42)", s)

        env['b'] = Integer(42.42)

        s = print_expression(Cons(Symbol('a'), Symbol('b')).eval(env))
        self.assertEquals("(123 . 42.42)", s)

        s = print_expression(Cons(Nil(), Nil()).eval(env))
        self.assertEquals("(())", s)

if __name__ == '__main__':
    unittest.main()
