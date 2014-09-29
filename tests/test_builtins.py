import unittest
from lispeln.scheme.builtins import define_builtins

from lispeln.scheme.constants import Float, Integer, Boolean, String
from lispeln.scheme.expressions import Environment, Call, Symbol


class BuiltInsTestCase(unittest.TestCase):
    def test_equals(self):

        env = Environment(None)
        define_builtins(env)

        env['a'] = Integer(1)
        env['b'] = Integer(5)

        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))

        env['b'] = Integer(1)
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))

        env['a'] = Boolean(True)
        env['b'] = Boolean(True)
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))

        env['a'] = Boolean(False)
        env['b'] = Boolean(False)
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))

        env['a'] = Boolean(False)
        env['b'] = Boolean(True)
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))

        env['a'] = String('test1')
        env['b'] = String('test1')
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))

        env['a'] = String('test1')
        env['b'] = String('test2')
        res = Call(Symbol('eq?'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))

    def test_comparisons(self):

        env = Environment(None)
        define_builtins(env)

        env['a'] = Integer(1)
        env['b'] = Integer(5)

        res = Call(Symbol('<'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))
        res = Call(Symbol('<='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))
        res = Call(Symbol('>'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))
        res = Call(Symbol('>='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))

        env['a'] = Integer(2)
        env['b'] = Integer(2)

        res = Call(Symbol('<'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))
        res = Call(Symbol('<='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))
        res = Call(Symbol('>'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))
        res = Call(Symbol('>='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))

        env['a'] = Integer(3)
        env['b'] = Integer(2)

        res = Call(Symbol('<'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))
        res = Call(Symbol('<='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(False))
        res = Call(Symbol('>'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))
        res = Call(Symbol('>='), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Boolean(True))


    def test_minus(self):

        env = Environment(None)
        define_builtins(env)

        env['a'] = Float(1.5)
        env['b'] = Float(0.3)
        res = Call(Symbol('-'), Symbol('a'), Symbol('b')).eval(env)
        self.assertEquals(res, Float(1.2))

        env['a'] = Integer(1.0)
        env['b'] = Float(2.3)
        res = Call(Symbol('-'), Symbol('a'), Symbol('b')).eval(env)
        self.assertAlmostEquals(res.value, Float(-1.3).value)

