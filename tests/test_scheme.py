from lispeln.scheme.constants import Integer, Float, String, Boolean

__author__ = 'schreon'

import unittest


class SchemeTestCase(unittest.TestCase):

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
if __name__ == '__main__':
    unittest.main()
