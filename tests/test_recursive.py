import unittest

from lispeln.evaluator.recursive import evaluate
from lispeln.evaluator.builtins import _plus, define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.scheme.constants import Integer
from lispeln.scheme.expressions import Symbol, Procedure
from lispeln.scheme.syntax import Lambda


def execute(code, env):
    return evaluate(parse(tokenize(code)), env)

class RecursiveEvaluatorTestCase(unittest.TestCase):
    """
    This test case tests the evaluator. It relies on the parser and scheme package being fully tested.
    """
    def test_symbol(self):
        # should have same object identity
        self.assertIs(Symbol("a"), Symbol("a"))
        # Symbol created by Symbol should work
        self.assertIs(Symbol("a"), Symbol(Symbol("a")))


    def test_environment(self):
        root = Environment(None, a=1, b=2)
        child1 = Environment(root, c=3)
        child2 = Environment(root, d=4)

        self.assertIn('a', child1)
        self.assertIn('b', child1)
        self.assertIn('c', child1)
        self.assertNotIn('d', child1)

        self.assertIn('a', child2)
        self.assertIn('b', child2)
        self.assertNotIn('c', child2)
        self.assertIn('d', child2)

        child1['a'] = 5
        self.assertEquals(child1['a'], 5)
        self.assertEquals(root['a'], 1)

    def test_procedure(self):

        env = Environment(None)
        self.assertEquals(_plus(Integer(1), Integer(2)), Integer(3))

        proc = Procedure(_plus)
        self.assertEquals(proc(Integer(1), Integer(2)), Integer(3))

        env['+'] = proc

        call = [Symbol('+'), Integer(1), Integer(2)]
        self.assertEquals(evaluate(call, env), Integer(3))

        call = [Symbol('+'), Integer(1), Integer(2), Integer(-2), Integer(100)]
        self.assertEquals(evaluate(call, env), Integer(101))

        env['a'] = Integer(10)
        env['b'] = Integer(-7)
        call = [Symbol('+'), Symbol('a'), Symbol('b')]
        self.assertEquals(evaluate(call, env), Integer(3))

    def test_lambda(self):
        env = Environment(None)
        define_builtins(env)
        env['n'] = Integer(42)

        actual = execute("((lambda (n) (set! n (+ n 1)) (set! n (* n 2)) n) 4)", env)
        expected = Integer(10)
        self.assertEquals(expected, actual)
        n = evaluate(Symbol('n'), env)
        self.assertEquals(n, Integer(42))

if __name__ == '__main__':
    unittest.main()
