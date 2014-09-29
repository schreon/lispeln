from lispeln.evluator import evaluate
from lispeln.printer.derived import print_cons, print_expression
from lispeln.scheme.builtins import _plus
from lispeln.scheme.constants import Nil, Integer, Boolean, Float, String
from lispeln.scheme.derived import Cons
from lispeln.scheme.environment import Symbol, Environment
from lispeln.scheme.procedure import Procedure, Lambda

__author__ = 'schreon'

import unittest
import logging

logging.basicConfig(level=logging.INFO)

class PrinterTestCase(unittest.TestCase):
    def test_numbers(self):
        i = Integer(1)
        f = Float(1.2)

        self.assertEquals("1", print_expression(i))
        self.assertEquals("1.2", print_expression(f))

    def test_string(self):
        s = String("Hallo Test String")
        self.assertEquals('"Hallo Test String"', print_expression(s))

    def test_boolean(self):
        t = Boolean(True)
        f = Boolean(False)

        self.assertEquals("#t", print_expression(t))
        self.assertEquals("#f", print_expression(f))

    def test_cons(self):

        env = Environment(None)
        env['a'] = Integer(123)
        env['b'] = Integer(42)

        expr = Cons(Symbol('a'), Symbol('b'))
        s = print_expression(evaluate(expr, env))
        self.assertEquals("(123 . 42)", s)

        env['b'] = Integer(42.42)

        s = print_expression(Cons(Symbol('a'), Symbol('b')).eval(env))
        self.assertEquals("(123 . 42.42)", s)

        s = print_expression(Cons(Nil(), Nil()).eval(env))
        self.assertEquals("(())", s)

        s = print_expression(Cons(Nil(), Cons(Nil(), Nil())).eval(env))
        self.assertEquals("(() ())", s)

        s = print_expression(Cons(Cons(Nil(), Nil()), Nil()).eval(env))
        self.assertEquals("((()))", s)

    def test_proc(self):
        env = Environment(None)
        env['a'] = Integer(1)
        env['b'] = Integer(5)
        env['c'] = Integer(-100)
        env['f'] = Procedure(_plus)

        l = Lambda([Symbol('c')], [Symbol('f'), Symbol('a'), Symbol('b'), Symbol('c')])
        s = print_expression(evaluate(l, env))
        self.assertEquals('#<procedure>', s)

        logging.info("Testing if procedure name is passed ...")
        env['g'] = Lambda([Symbol('c')], [Symbol('f'), Symbol('a'), Symbol('b'), Symbol('c')])
        s = print_expression(Symbol('g').eval(env))
        self.assertEquals('#<procedure:g>', s)

        logging.info("Testing if procedure name sticks ...")
        env['h'] = Symbol('g').eval(env)
        env['g'] = Integer(5)
        s1 = print_expression(env['g'].eval(env))
        self.assertEquals('5', s1)
        s2 = print_expression(env['h'].eval(env))
        self.assertEquals('#<procedure:g>', s2)


if __name__ == '__main__':
    unittest.main()
