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

    def test_pair(self):
        expr = Pair(Integer(1), Pair(Integer(2), Pair(Integer(3), Nil())))
        expected = "(1 2 3)"
        self.assertEquals(expected, print_expression(expr))

        expr = Pair(Integer(1), Pair(Integer(2), Pair(Integer(3), Integer(4))))
        expected = "(1 2 3 . 4)"
        self.assertEquals(expected, print_expression(expr))

    def test_quote(self):
        actual = echo("' ( cons 1 (  cons 2 (cons 3 '() ) )  )")
        expected = "(cons 1 (cons 2 (cons 3 '())))"

        logging.info(repr(actual))
        self.assertEquals(expected, actual)

    def test_nil(self):
        actual = echo("'(cons 1 '())")
        expected = "(cons 1 '())"
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
