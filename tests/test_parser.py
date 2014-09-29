from lispeln.parser.scanner import Scanner

__author__ = 'schreon'

import unittest


class Parser(object):
    def __init__(self,):
        super(Parser, self).__init__()

    def parse(self, string):
        scanner = Scanner(string)

class ParserTestCase(unittest.TestCase):
    def test_initialization(self):
        """
        it does initialize correctly
        """
        Parser()

    def test_plus(self):
        """
        it parses (+ 1 2)
        """
        parser = Parser()
        output = parser.parse("(+ 1 2)")



if __name__ == '__main__':
    unittest.main()
