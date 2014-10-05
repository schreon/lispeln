from lispeln.scheme.constants import Integer, Float, String, Boolean


import unittest


class SchemeTestCase(unittest.TestCase):
    """
    This test case tests the scheme AST objects itself. It is isolated from all other packages.
    """

    def test_assignment(self):
        pass

    def test_constants(self):
        Integer(42)
        self.assertRaises(Exception, Integer, 42.42)
        self.assertRaises(Exception, Integer, "42.42")
        Float(42.5)
        self.assertRaises(Exception, Float, 42)
        String("Correct")
        self.assertRaises(Exception, String, 42)
        self.assertRaises(Exception, String, 42.5)
        Boolean(True)
        Boolean(False)
        self.assertRaises(Exception, Boolean, 42)
        self.assertRaises(Exception, Boolean, 42.5)
        self.assertRaises(Exception, Boolean, "True")
        self.assertRaises(Exception, Boolean, "False")

    def test_derived(self):
        pass

    def test_expression(self):
        pass

    def test_logic(self):
        pass

    def test_procedure(self):
        pass

if __name__ == '__main__':
    unittest.main()
