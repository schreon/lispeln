from lispeln.evaluator.recursive import evaluate
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.scheme import print_expression
from lispeln.scheme.constants import Nil, Integer, Boolean, Float, String
from lispeln.scheme.derived import Pair
from lispeln.scheme.procedure import Procedure, Lambda
from lispeln.scheme.symbol import Symbol


import unittest
import logging

logging.basicConfig(level=logging.INFO)


def echo(code):
    return print_expression(parse(tokenize(code)))


class PrinterTestCase(unittest.TestCase):
    """
    This is the printer test case. It relies on the following packages to be fully tested: parser, scheme
    """
    def test_numbers(self):
        self.assertEquals("1", echo("1"))
        self.assertEquals("1.2", echo("1.2"))

    def test_string(self):
        self.assertEquals('"Hallo Test String"', echo('"Hallo Test String"'))

    def test_boolean(self):
        self.assertEquals('#t', echo('#t'))
        self.assertEquals('#f', echo('#f'))
        self.assertEquals('#t', echo('true'))
        self.assertEquals('#f', echo('false'))

    def test_cons(self):
        inp = "( cons 1 (  cons 2 (cons 3 '() ) )  )"
        expected = "(1 2 3)"
        self.assertEquals(expected, echo(inp))

        inp = " ( cons 1 ( cons 2 (  cons 3 4)))"
        expected = "(1 2 3 . 4)"
        self.assertEquals(expected, echo(inp))

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
        s = print_expression(evaluate(Symbol('g'), env))
        self.assertEquals('#<procedure:g>', s)

        logging.info("Testing if procedure name sticks ...")
        env['h'] = evaluate(Symbol('g'), env)
        env['g'] = Integer(5)
        s1 = print_expression(evaluate(Symbol('g'), env))
        self.assertEquals('5', s1)
        s2 = print_expression(evaluate(Symbol('h'), env))
        self.assertEquals('#<procedure:g>', s2)


if __name__ == '__main__':
    unittest.main()
