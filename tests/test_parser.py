import logging
from lispeln.evaluator.recursive import evaluate
from lispeln.parser.tokenizer import tokenize
from lispeln.parser.parser import parse
from lispeln.printer.derived import print_expression
from lispeln.scheme.builtins import define_builtins
from lispeln.scheme.constants import Integer
from lispeln.scheme.derived import Begin
from lispeln.scheme.environment import Environment, Symbol
from lispeln.scheme.procedure import Call

__author__ = 'schreon'

import unittest

logging.basicConfig(level=logging.INFO)

class ParserTestCase(unittest.TestCase):

    def test_tokenizer(self):
        self.assertEquals(tokenize("(+ 1 2)"), ['+', '1', '2'])
        self.assertEquals(tokenize("(+ (1 2))"), ['+', ['1', '2']])
        self.assertEquals(tokenize("1"), ['1'])

    def test_parser(self):
        parsed = parse(tokenize("(+ 1 2)"))

        env = Environment(None)
        define_builtins(env)

        expected = evaluate(Begin(Call(Symbol('+'), Integer(1), Integer(2))), env)
        actual = evaluate(parsed, env)
        self.assertEquals(expected, actual)

        actual = evaluate(parse(tokenize("5")), env)
        expected = Integer(5)
        self.assertEquals(expected, actual)

    def test_begin(self):
        env = Environment(None)

        actual = evaluate(parse(tokenize("(begin (define x 1) (+ x 2))")), env)
        expected = Integer(3)
        self.assertEquals(expected, actual)

    def test_lambda(self):
        env = Environment(None)
        define_builtins(env)

        env['n'] = Integer(42)

        tokens = tokenize("((lambda (n) (set! n 42) (+ n 1)) n)")

        logging.info(tokens)

        expression = parse(tokens)
        actual = evaluate(expression, env)
        expected = Integer(43)
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
