import unittest

from lispeln.evaluator.recursive import evaluate
from lispeln.evaluator.builtins import _plus, define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.scheme.constants import Integer, Boolean, Nil, String
from lispeln.scheme.expressions import Symbol, Procedure, Pair

def execute(code, env):
    res = None
    for toks in tokenize(code):
        res = evaluate(parse(toks), env)
    return res

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

    def test_constants(self):
        env = Environment(None)

        execute("1", env)
        execute("+1", env)
        execute("-1", env)
        execute("1.5", env)
        execute("+1.5", env)
        execute("-1.5", env)

        expected = String(" this is a nice string\n ; yes 123 ")
        actual = execute('" this is a nice string\n ; yes 123 "', env)
        self.assertEquals(expected, actual)

        execute('#t', env)
        execute('#f', env)


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

    def test_let(self):
        env = Environment(None)
        define_builtins(env)

        actual = execute("(let ((x 2) (y 3)) (* x y))", env)
        expected = Integer(6)
        self.assertEquals(expected, actual)

    def test_named_lambda(self):
        env = Environment(None)
        define_builtins(env)
        execute("(define add1 (lambda (x) (+ x 1)))", env)
        proc = execute("add1", env)
        self.assertEquals("add1", proc.name)

    def test_lambda(self):
        env = Environment(None)
        define_builtins(env)
        env['n'] = Integer(42)

        actual = execute("((lambda (n) (set! n (+ n 1)) (set! n (* n 2)) n) 4)", env)
        expected = Integer(10)
        self.assertEquals(expected, actual)
        n = evaluate(Symbol('n'), env)
        self.assertEquals(n, Integer(42))

    def test_proc_lambda(self):
        env = Environment(None)
        define_builtins(env)

        execute("(define x (lambda (a) (if (eq? a #t) + -)))", env)
        self.assertEquals(Integer(7), execute("((x #t) 3 4)", env))

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

        self.assertEquals(repr(Symbol('a')), repr(execute("' a ;123 '(test", env)))
        self.assertEquals(repr([Symbol('a')]), repr(execute("' (a) ;123 '(test", env)))
        self.assertEquals(repr(Symbol('a')), repr(execute("(quote a)", env)))
        self.assertEquals(repr([Symbol('a')]), repr(execute("(quote (a))", env)))
        self.assertEquals(repr(parse(tokenize("(  1  2 3 )")[0])), repr(execute("( quote ( 1 2 3    ))", env)))

    def test_pairs(self):
        env = Environment(None)
        define_builtins(env)

        execute("(define l (cons (cons 1 2) 3))", env)
        execute("(define f (car l))", env)
        execute("(define r (cdr l))", env)

        l = execute("l", env)
        f = execute("f", env)
        r = execute("r", env)

        self.assertEquals(Pair(Pair(Integer(1), Integer(2)), Integer(3)), l)
        self.assertEquals(Pair(Integer(1), Integer(2)), f)
        self.assertEquals(Integer(3), r)

    def test_multiple_define(self):
        env = Environment(None)
        define_builtins(env)

        execute("""
            (define a 1)
            (define b 2)
            (define c 3)
            (define d 4)
             """, env)

        self.assertEquals(env['a'], Integer(1))
        self.assertEquals(env['b'], Integer(2))
        self.assertEquals(env['c'], Integer(3))
        self.assertEquals(env['d'], Integer(4))

    def test_set_test(self):
        """
        Test von Julius adaptiert: https://github.com/juliusf/schemePy/blob/master/tests/evaluator_tests.py#L266
        """
        env = Environment(None)
        define_builtins(env)

        execute("""
            (define singletonSet (lambda (x) (lambda (y) (= y x))))
            (define contains (lambda (set_ y) (set_ y)))
            (define s1 (singletonSet 1))
            (define s2 (singletonSet 2))
            (define s3 (lambda (x) (and (>= x 5) (<= x 15))))
            (define s4 (lambda (x) (and (<= x -5) (>= x -15))))
             """, env)

        self.assertEquals(Boolean(True), execute("(contains s1 1)", env))
        self.assertEquals(Boolean(True), execute("(contains s2 2)", env))
        self.assertEquals(Boolean(True), execute("(contains s3 5)", env))
        self.assertEquals(Boolean(True), execute("(contains s4 -5)", env))
        self.assertEquals(Boolean(False), execute("(contains s4 -22)", env))

    def test_y_combinator(self):
        """
        Test von Julius adaptiert: https://github.com/juliusf/schemePy/blob/master/tests/evaluator_tests.py#L314
        """
        env = Environment(None)
        define_builtins(env)

        execute("""
            (define Y
             (lambda (f)
             ((lambda (x) (x x))
             (lambda (g)
             (f (lambda (x) ((g g) x)))))))
               (define fac
                 (Y
                   (lambda (f)
                     (lambda (x)
                       (if (< x 2)
                           1
                           (* x (f (- x 1))))))))
        """, env)

        self.assertEquals(Integer(720), execute("(fac 6)", env))


    def test_iota(self):
        """
        Test von Julius adaptiert: https://github.com/juliusf/schemePy/blob/master/tests/evaluator_tests.py#L337
        """
        env = Environment(None)
        define_builtins(env)

        execute("""
            (define iota
                (lambda (start end step)
                    (begin
                        (define helper
                            (lambda (cur list)
                                (if (= cur start)
                                    list
                                    (helper
                                        (- cur step)
                                        (cons cur list)))))
                        (helper end '()))))
            """, env)

        res = execute("(iota 10 1 -1)", env)
        expected = Pair(Integer(9),
                        Pair(Integer(8),
                             Pair(Integer(7),
                                  Pair(Integer(6),
                                       Pair(Integer(5),
                                            Pair(Integer(4),
                                                 Pair(Integer(3),
                                                      Pair(Integer(2),
                                                           Pair(Integer(1),
                                                                Nil())
                                                      )
                                                 )
                                            )
                                       )
                                  )
                             )
                        )
        )
        self.assertEquals(expected, res)


if __name__ == '__main__':
    unittest.main()
