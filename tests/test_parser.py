
from lispeln.parser.tokenizer import tokenize
from lispeln.parser.parser import parse

import unittest

class ParserTestCase(unittest.TestCase):
    """
    This test case tests the parser. It relies on the scanner package to be fully tested.
    """

    def test_tokenizer(self):
        self.assertEquals(tokenize("( + 1 2 )"), [['+', '1', '2']])
        self.assertEquals(tokenize("(+ ( 1 2 ) )"), [['+', ['1', '2']]])
        self.assertEquals(tokenize("1 "), ['1'])

    def test_parser(self):
        actual = repr(parse(tokenize("(begin ( + 1 2 ))")))
        expected = "[[<Syntax:Begin>, [<Symbol:+>, <Integer:1>, <Integer:2>]]]"
        self.assertEquals(expected, actual)

        actual = repr(parse(tokenize("(begin (define x 1) (+ x 2))")))
        expected = "[[<Syntax:Begin>, [<Syntax:Define>, <Symbol:x>, <Integer:1>], [<Symbol:+>, <Symbol:x>, <Integer:2>]]]"
        self.assertEquals(expected, actual)

        actual = repr(parse(tokenize("((lambda (n) (set! n 42) (+ n 1)) n)")))
        expected = "[[[<Syntax:Lambda>, [<Symbol:n>], [<Syntax:Set>, <Symbol:n>, <Integer:42>], [<Symbol:+>, <Symbol:n>, <Integer:1>]], <Symbol:n>]]"
        self.assertEquals(expected, actual)

    def test_comment(self):
        string = "(+ 1\n; test comment with whitespace\n3)"
        tokens = tokenize(string)
        self.assertEquals(tokens, [['+', '1', '3']])


if __name__ == '__main__':
    unittest.main()
