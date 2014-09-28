import unittest
from lispeln.constants import Integer, Float, String, Boolean, Nil
from lispeln.expressions import Procedure


class SchemeTypesTestCase(unittest.TestCase):

    def test_int(self):
        x = Integer(42)
        self.assertEquals(repr(x), "<Integer:42>")
        self.assertEquals(str(x), "42")

    def test_float(self):
        x = Float(42.42)
        self.assertEquals(repr(x), "<Float:42.42>")
        self.assertEquals(str(x), "42.42")

    def test_string(self):
        x = String('eins Zwei DREI')
        self.assertEquals(repr(x), '<String:eins Zwei DREI>')
        self.assertEquals(str(x), '"eins Zwei DREI"')
        String('bla bla bla')

    def test_boolean(self):
        x = Boolean(True)
        self.assertEquals(repr(x), "<Boolean:true>")
        self.assertEquals(str(x), "#t")
        x = Boolean(False)
        self.assertEquals(repr(x), "<Boolean:false>")
        self.assertEquals(str(x), "#f")

    def test_nil(self):
        x = Nil()
        self.assertEquals(repr(x), "<Nil>")
        self.assertEquals(str(x), "'()")

    def test_procedure(self):
        proc = Procedure('my_procedure', ['-', 3, 4])
        self.assertEquals(repr(proc), "<Procedure:my_procedure>")
        self.assertEquals(str(proc), "my_procedure")




if __name__ == '__main__':
    unittest.main()
