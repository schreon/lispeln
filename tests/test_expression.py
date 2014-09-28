from lispeln.types import Integer, Float, Environment

__author__ = 'schreon'

import unittest


class Expression(object):
    pass

class Procedure(object):

    def __init__(self, name, operand, *args):
        self.name = name
        self.operand = operand
        self.args = args

    def eval(self, environment):
        args = [environment.eval(arg) for arg in self.args]
        return self.operand(*args)

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
    def test_expression(self):

        env = Environment(None)
        self.assertEquals(plus(Integer(1), Integer(2)), Integer(3))

        proc = Procedure('+', plus, Integer(1), Integer(2))
        self.assertEquals(proc.eval(env), Integer(3))

        #expr = Expression(plus, Integer("1"), Integer("2"))
        #self.assertEquals(expr.eval(), Integer("3"))


if __name__ == '__main__':
    unittest.main()
