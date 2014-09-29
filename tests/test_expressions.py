import unittest
from lispeln.scheme.builtins import _plus

from lispeln.scheme.constants import Integer, Boolean, Float
from lispeln.scheme.expressions import Symbol, Environment, Procedure, Call, Lambda, Conditional, Define, Set, And


class ExpressionTestCase(unittest.TestCase):
    def test_symbol(self):
        x = Symbol("test")
        self.assertEquals(repr(x), "<Symbol:test>")
        self.assertEquals(str(x), "'test")
        Symbol("test123")
        Symbol("test_123")
        Symbol("test!")

        # should have same object identity
        self.assertIs(Symbol("a"), Symbol("a"))
        # Symbol created by Symbol should work
        self.assertIs(Symbol("a"), Symbol(Symbol("a")))

    def test_environment(self):
        root = Environment(None, a=1, b=2)

        for key, val in root.iteritems():
            self.assertIsInstance(key, Symbol)
            self.assertIn(val, [1, 2])

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
        self.assertEquals(call.eval(env), Integer(3))

        call = Call(Symbol('+'), Integer(1), Integer(2), Integer(-2), Integer(100))
        self.assertEquals(call.eval(env), Integer(101))

        env['a'] = Integer(10)
        env['b'] = Integer(-7)
        call = Call(Symbol('+'), Symbol('a'), Symbol('b'))
        self.assertEquals(call.eval(env), Integer(3))

    def test_lambda(self):

        env = Environment(None)
        env['a'] = Integer(1)
        env['b'] = Integer(5)
        env['c'] = Integer(-100)
        env['f'] = Procedure(_plus)
        env['g'] = Lambda([Symbol('c')], [Symbol('f'), Symbol('a'), Symbol('b'), Symbol('c')])

        env['x'] = Integer(50)
        call = Call(Symbol('g'), Symbol('x'))
        self.assertEquals(call.eval(env), Integer(56))
        env['x'] = Integer(10)
        self.assertEquals(call.eval(env), Integer(16))

    def test_conditional(self):
        env = Environment(None)
        env['a'] = Integer(1)
        env['b'] = Integer(5)

        self.assertEquals(Conditional(Boolean(True), Symbol('a'), Symbol('b')).eval(env), Integer(1))
        self.assertEquals(Conditional(Boolean(False), Symbol('a'), Symbol('b')).eval(env), Integer(5))

    def test_define(self):
        env = Environment(None)
        Define(Symbol('a'), Integer(42)).eval(env)

        self.assertEquals(env['a'], Integer(42))

    def test_set(self):
        set_ = Set(Symbol('a'), Integer(666))

        env = Environment(None)

        self.assertRaises(Exception, set_.eval, env)

        Define(Symbol('a'), Integer(42)).eval(env)
        self.assertEquals(env['a'], Integer(42))

        set_.eval(env)
        self.assertEquals(env['a'], Integer(666))

    def test_quote(self):
        env = Environment(None)


        # TODO: test quote
        # TODO: implement external representations

    def test_and(self):

        env = Environment(None)

        env['a'] = Float(1.5)
        env['b'] = Float(0.3)

        res = And(Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Symbol('b').eval(env))

        env['a'] = Boolean(False)

        res = And(Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))

        env['a'] = Boolean(True)

        res = And(Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Symbol('b').eval(env))

        res = And().eval(env)
        self.assertEquals(res, Boolean(True))


if __name__ == '__main__':
    unittest.main()
