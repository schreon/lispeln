import unittest
from lispeln.types import Type, Integer, Float, String, Symbol, InvalidValueException, Boolean, Nil, Cons, Procedure, \
    Environment


class SchemeTypesTestCase(unittest.TestCase):
    def test_base_type(self):
        x = Type("test")
        self.assertEquals(repr(x), "<Type:test>")
        self.assertEquals(str(x), "test")

    def test_int(self):
        x = Integer(42)
        self.assertEquals(repr(x), "<Integer:42>")
        self.assertEquals(str(x), "42")

    def test_float(self):
        x = Float(42.42)
        self.assertEquals(repr(x), "<Float:42.42>")
        self.assertEquals(str(x), "42.42")
        self.assertRaises(InvalidValueException, Float, '"test"')

    def test_string(self):
        x = String('eins Zwei DREI')
        self.assertEquals(repr(x), '<String:eins Zwei DREI>')
        self.assertEquals(str(x), '"eins Zwei DREI"')
        String('bla bla bla')

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

    def test_boolean(self):
        x = Boolean(True)
        self.assertEquals(repr(x), "<Boolean:true>")
        self.assertEquals(str(x), "#t")
        x = Boolean(False)
        self.assertEquals(repr(x), "<Boolean:false>")
        self.assertEquals(str(x), "#f")
        self.assertRaises(InvalidValueException, Boolean, '123')
        self.assertRaises(InvalidValueException, Boolean, 'abc')
        self.assertRaises(InvalidValueException, Boolean, '!?=')

    def test_nil(self):
        x = Nil()
        self.assertEquals(repr(x), "<Nil>")
        self.assertEquals(str(x), "'()")

    def test_cons(self):
        a, b = Symbol("a"), Symbol("b")
        x = Cons(a, b)
        self.assertEquals(repr(x), "<Cons: ('a.'b)>")
        self.assertEquals(str(x), "('a . 'b)")
        self.assertEquals(x.first, a)
        self.assertEquals(x.rest, b)

        x = Cons(a, Cons(a, Cons(a, b)))
        self.assertEquals(x.ravel(), [a, a, a, b])
        self.assertEquals(str(x), "('a 'a 'a . 'b)")

        x = Cons(a, Cons(Cons(a, b), Cons(a, b)))
        self.assertEquals(str(x), "('a ('a . 'b) 'a . 'b)")

        x = Cons(a, Cons(b, Nil()))
        self.assertEquals(str(x), "('a 'b)")

    def test_procedure(self):
        proc = Procedure('my_procedure', ['-', 3, 4])
        self.assertEquals(repr(proc), "<Procedure:my_procedure>")
        self.assertEquals(str(proc), "my_procedure")
        self.assertEquals(proc.implementation, ['-', 3, 4])

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


if __name__ == '__main__':
    unittest.main()
