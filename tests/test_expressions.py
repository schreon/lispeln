from lispeln.types import Integer, Float, Environment, Symbol

__author__ = 'schreon'

import unittest



def plus(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s" % str(type(arg)))
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

    def test_expression(self):

        env = Environment(None)
        self.assertEquals(plus(Integer(1), Integer(2)), Integer(3))

        proc = Procedure('+', plus, Integer(1), Integer(2))
        self.assertEquals(proc.eval(env), Integer(3))

        env['+'] = proc
        expr = Expression(Symbol('+'), Integer(1), Integer(2))
        self.assertEquals(expr.eval(env), Integer(3))


if __name__ == '__main__':
    unittest.main()
