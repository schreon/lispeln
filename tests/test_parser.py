import logging
from lispeln.parser.tokenizer import tokenize
from lispeln.parser.parser import parse

__author__ = 'schreon'

import unittest

logging.basicConfig(level=logging.INFO)

class ParserTestCase(unittest.TestCase):

    def test_tokenizer(self):
        self.assertEquals(tokenize("(+ 1 2)"), ['+', '1', '2'])
        self.assertEquals(tokenize("(+ (1 2))"), ['+', ['1', '2']])
        self.assertEquals(tokenize("1"), ['1'])


if __name__ == '__main__':
    unittest.main()
