from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.quote import quote_expression

__author__ = 'schreon'

import unittest

import logging

logging.basicConfig(level=logging.INFO)

def echo(code):
    tokens = tokenize(code)
    logging.info(tokens)
    expression = parse(tokens)
    logging.info(repr(expression))
    return quote_expression(expression)

class QuoteTestCase(unittest.TestCase):
    """
    This test case tests the quote-printer.
    """
    def test_let(self):
        self.assertEquals("let", echo("'let"))
        self.assertEquals("(let)", echo("'(let)"))


if __name__ == '__main__':
    unittest.main()
