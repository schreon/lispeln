import unittest
from lispeln.evaluator.recursive import evaluate
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.builtins import _plus, define_builtins
from lispeln.scheme.derived import Let, Begin
from lispeln.scheme.environment import Symbol, Environment
from lispeln.scheme.logic import If, And

from lispeln.scheme.constants import Integer, Boolean, Float, String
from lispeln.scheme.procedure import Procedure, Call, Lambda

class ExpressionTestCase(unittest.TestCase):
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

        call = Call(Symbol('+'), Integer(1), Integer(2))
        self.assertEquals(evaluate(call, env), Integer(3))

        call = Call(Symbol('+'), Integer(1), Integer(2), Integer(-2), Integer(100))
        self.assertEquals(evaluate(call, env), Integer(101))

        env['a'] = Integer(10)
        env['b'] = Integer(-7)
        call = Call(Symbol('+'), Symbol('a'), Symbol('b'))
        self.assertEquals(evaluate(call, env), Integer(3))

    def test_lambda(self):

        env = Environment(None)
        define_builtins(env)

        env['a'] = Integer(1000)
        env['b'] = Integer(100)
        env['c'] = Integer(10)
        env['g'] = Lambda([Symbol('c')], [Symbol('+'), Symbol('a'), Symbol('b'), Symbol('c')])

        env['x'] = Integer(1)
        call = Call(Symbol('g'), Symbol('x'))

        self.assertEquals(evaluate(call, env), Integer(1101))
        env['x'] = Float(0.5)
        self.assertEquals(evaluate(call, env), Float(1100.5))

    def test_conditional(self):
        env = Environment(None)
        env['a'] = Integer(1)
        env['b'] = Integer(5)

        self.assertEquals(evaluate(If(Boolean(True), Symbol('a'), Symbol('b')), env), Integer(1))
        self.assertEquals(evaluate(If(Boolean(False), Symbol('a'), Symbol('b')), env), Integer(5))

    def test_define(self):
        env = Environment(None)
        evaluate(Define(Symbol('a'), Integer(42)), env)

        self.assertEquals(env['a'], Integer(42))

    def test_set(self):
        set_ = Set(Symbol('a'), Integer(666))

        env = Environment(None)

        self.assertRaises(Exception, evaluate, (set_, env))

        evaluate(Define(Symbol('a'), Integer(42)), env)
        self.assertEquals(env['a'], Integer(42))

        evaluate(set_, env)
        self.assertEquals(env['a'], Integer(666))

    def test_quote(self):
        env = Environment(None)


        # TODO: test quote
        # TODO: implement external representations

    def test_and(self):

        env = Environment(None)

        env['a'] = Float(1.5)
        env['b'] = Float(0.3)

        res = evaluate(And(Symbol('a'), Symbol('b')), env)
        self.assertEquals(res, evaluate(Symbol('b'), env))

        env['a'] = Boolean(False)

        res = evaluate(And(Symbol('a'), Symbol('b')), env)
        self.assertEquals(res, Boolean(False))

        env['a'] = Boolean(True)

        res = evaluate(And(Symbol('a'), Symbol('b')), env)
        self.assertEquals(res, evaluate(Symbol('b'), env))

        res = evaluate(And(), env)
        self.assertEquals(res, Boolean(True))

    def test_let(self):
        env = Environment(None)
        env['+'] = Procedure(_plus)
        env['y'] = Integer(1)

        let = Let([(Symbol('x'), Integer(10))], Call(Symbol('+'), Symbol('x'), Symbol('y')))

        self.assertEquals(evaluate(let, env), Integer(11))
        self.assertNotIn(Symbol('x'), env)

    def test_begin(self):
        env = Environment(None)

        begin = Begin(
            Define(Symbol('a'), Integer(42)),
            Define(Symbol('b'), Integer(-42)),
            Call(Procedure(_plus), Symbol('a'), Symbol('b'))
        )

        self.assertEquals(evaluate(begin, env), Integer(0))
if __name__ == '__main__':
    unittest.main()
