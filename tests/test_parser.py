import logging

from lispeln.evaluator.recursive import evaluate
from lispeln.parser.tokenizer import tokenize
from lispeln.parser.parser import parse
from lispeln.evaluator.builtins import define_builtins
from lispeln.scheme.constants import Integer, Boolean
from lispeln.scheme.derived import Begin, Pair
from lispeln.evaluator.environment import Environment
from lispeln.scheme.procedure import Call
from lispeln.scheme.symbol import Symbol


__author__ = 'schreon'

import unittest

logging.basicConfig(level=logging.INFO)

def execute(code, env):
    return evaluate(parse(tokenize(code)), env)

class ParserTestCase(unittest.TestCase):
    """
    This test case tests the parser. It relies on the scanner package to be fully tested.
    """
    def test_tokenizer(self):
        self.assertEquals(tokenize("(+ 1 2)"), ['+', '1', '2'])
        self.assertEquals(tokenize("(+ (1 2))"), ['+', ['1', '2']])
        self.assertEquals(tokenize("1"), '1')

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
        define_builtins(env)

        actual = execute("(begin (define x 1) (+ x 2))", env)
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

        code = "((lambda (n) (set! n (+ n 1)) (set! n (* n 2)) n) 4)"
        tokens = tokenize(code)
        expression = parse(tokens)
        actual = evaluate(expression, env)
        expected = Integer(10)
        self.assertEquals(expected, actual)
        n = evaluate(Symbol('n'), env)
        self.assertEquals(n, Integer(42))

    def test_comment(self):

        string = "(+ 1\n; test comment with whitespace\n3)"
        tokens = tokenize(string)
        self.assertEquals(tokens, ['+', '1', '3'])

    def test_let(self):
        env = Environment(None)
        define_builtins(env)

        code = "(let ((x 2) (y 3)) (* x y))"
        tokens = tokenize(code)
        expression = parse(tokens)
        actual = evaluate(expression, env)
        expected = Integer(6)
        self.assertEquals(expected, actual)

    def test_and(self):
        env = Environment(None)
        define_builtins(env)

        self.assertEquals(Boolean(True), execute("(and (= 2 2) (> 2 1))", env))
        self.assertEquals(Boolean(False), execute("(and (= 2 2) (< 2 1))", env))
        self.assertEquals(Integer(10), execute("(and 1 2 5 10) ", env))
        self.assertEquals(Boolean(True), execute("(and)", env))

    def test_or(self):
        env = Environment(None)
        define_builtins(env)

        self.assertEquals(Boolean(True), execute("(or (= 2 2) (> 2 1))", env))
        self.assertEquals(Boolean(True), execute("(or (= 2 2) (< 2 1))", env))
        self.assertEquals(Boolean(False), execute("(or #f #f #f)", env))

    def _case(self):
        # TODO
        env = Environment(None)
        define_builtins(env)

        self.assertEquals(Boolean(True), execute("(* 2 3)", env))
        self.assertEquals(Boolean(True), execute("(or (= 2 2) (< 2 1))", env))
        self.assertEquals(Boolean(False), execute("(or #f #f #f)", env))

    def test_proc_lambda(self):
        env = Environment(None)
        define_builtins(env)

        execute("(define x (lambda (a) (if (eq? a #t) + -)))", env)
        self.assertEquals(Integer(7), execute("((x #t) 3 4)", env))

    def test_cons(self):
        env = Environment(None)
        define_builtins(env)

        self.assertEquals(Pair(Pair(Integer(1), Integer(2)), Integer(3)), execute("(cons (cons 1 2) 3)", env))
        self.assertEquals(Pair(Integer(3), Pair(Integer(1), Integer(2))), execute("(cons 3 (cons 1 2))", env))

        self.assertEquals(Integer(1), execute("(car (cons 1 2))", env))
        self.assertEquals(Integer(2), execute("(cdr (cons 1 2))", env))

    def test_quote(self):

        env = Environment(None)
        define_builtins(env)

        tokens = tokenize("' a ;123 '(test")
        self.assertEquals(["'", "a"], tokens)
        expression = parse(tokens)
        self.assertEquals(repr(Symbol('a')), repr(evaluate(expression, env)))

if __name__ == '__main__':
    unittest.main()
