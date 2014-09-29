import unittest
from lispeln.constants import Float, Integer
from lispeln.expressions import Symbol, Environment, Procedure, Expression, Call, Lambda


def plus(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    s = sum(arg.value for arg in args)
    if type(s) == float:
        return Float(s)
    if type(s) == int:
        return Integer(s)
    raise Exception("Invalid result type: %s" % str(type(s)))

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
        self.assertEquals(plus(Integer(1), Integer(2)), Integer(3))

        proc = Procedure(plus)
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
        env['f'] = Procedure(plus)
        env['g'] = Lambda([Symbol('c')], [Symbol('f'), Symbol('a'), Symbol('b'), Symbol('c')])

        env['x'] = Integer(50)
        call = Call(Symbol('g'), Symbol('x'))
        self.assertEquals(call.eval(env), Integer(56))


if __name__ == '__main__':
    unittest.main()
