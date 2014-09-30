import unittest
from lispeln.evluator import evaluate, Promise, resolve
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
        n = 20
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
        res.resolve()
        end_time = time.time()
        logging.info("Resolve took %.2f seconds" % (end_time-start_time))

        logging.info(print_expression(res))

    def test_call(self):

        env = Environment(None)
        define_builtins(env)

        env['x'] = Integer(5)
        env['y'] = Integer(1)
        f1 = Call(Symbol('+'), Symbol('x'), Symbol('y'))

        res = evaluate(f1, env)
        resolve()

        print_expression(res)