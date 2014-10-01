import unittest
from lispeln.evaluator import evaluate, Promise
from lispeln.printer.derived import print_expression
from lispeln.scheme.assignment import Define
from lispeln.scheme.builtins import define_builtins
from lispeln.scheme.constants import Integer, Float
from lispeln.scheme.derived import Cons

import logging
from lispeln.scheme.environment import Environment, Symbol
from lispeln.scheme.procedure import Lambda, Call, Procedure

logging.basicConfig(level=logging.INFO)

import time

class ContinuationTestCase(unittest.TestCase):

    def off(self):

        env = Environment(None)

        start_time = time.time()
        n = 10000
        env['s0'] = Integer(42)
        for x in xrange(1, n):
            env['s%d' % x] = Symbol('s%d' % (x-1))
        end_time = time.time()
        logging.info("finished initializing environment, which took %.2f seconds" % (end_time - start_time))

        start_time = time.time()
        res = evaluate(Symbol('s%d' % (n-1)), env)
        end_time = time.time()
        logging.info("First evaluate took %.2f seconds" % (end_time-start_time))
        start_time = time.time()
        res = res.resolve()
        end_time = time.time()
        logging.info("Resolve took %.2f seconds" % (end_time-start_time))

        logging.info(print_expression(res))

    def test(self):

        env = Environment(None)
        define_builtins(env)

        n = 100

        env['x'] = Integer(0)
        env['y'] = Integer(1)

        env['f0'] = Call(Symbol('+'), Symbol('x'), Symbol('y'))
        for n in xrange(n):
            prev_key = 'f%d' % n
            next_key = 'f%d' % (n+1)
            env[next_key] = Call(Symbol('+'), Symbol(prev_key), Symbol('y'))

        res = evaluate(None, Symbol(next_key), env)
        res = res.resolve()

        print_expression(res)



    def off(self):
        env = Environment(None)
        define_builtins(env)

        env['f'] = Symbol('g')
        env['g'] = Symbol('f')

        res = evaluate(Symbol('f'), env)
        resolve(res)

        print_expression(res)


    def off(self):
        env = Environment(None)
        define_builtins(env)

        env['a'] = Call(Symbol('+'), Symbol('x'), Symbol('y'))
        env['b'] = Symbol('a')
        env['f'] = Symbol('b')
        env['y'] = Integer(100)
        env['x'] = Integer(200)
        res = evaluate(Symbol('f'), env)
        resolve(res)

        print_expression(res)

    def off(self):

        env = Environment(None)
        define_builtins(env)

        n = 100

        env['a'] = Integer(1)
        env['b'] = Integer(5)
        env['c'] = Integer(-100)

        env['g'] = Lambda([Symbol('c')], [Symbol('+'), Symbol('a'), Symbol('b'), Symbol('c')])

        env['x'] = Integer(50)
        call = Call(Symbol('g'), Symbol('x'))
        res = evaluate(call, env)
        resolve(res)

        self.assertEquals(res, Integer(56))

        print_expression(res)