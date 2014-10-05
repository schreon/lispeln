import unittest

from lispeln.parser.scanner import Scanner, UnexpectedCharacterException, UnexpectedEndOfStringException

import logging
from lispeln.parser.tokenizer import tokenize

logging.basicConfig(level=logging.INFO)
class ScannerTestCase(unittest.TestCase):
    """
    This test case tests the scanner. It is isolated form all other packages.
    """
    def test_initialize(self):
        """
        it does initialize correctly
        """
        string = ""
        scanner = Scanner(string)
        self.assertIsNotNone(scanner)

    def test_seek(self):
        """
        it does seek correctly
        """
        string = "dies ist \n  ein Test"
        scanner = Scanner(string)
        for i in xrange(len(string)):
            self.assertEquals(scanner.seek(i), string[i])

    def test_peek(self):
        """
        it does peek correctly
        """
        string = "dies ist \n  ein Test"
        scanner = Scanner(string)
        for i in xrange(len(string)):
            self.assertEquals(scanner.peek(i), string[i])

    def test_next(self):
        """
        it does traverse a string using the next method
        """
        string = "dies ist \n  ein Test"
        scanner = Scanner(string)
        for i in xrange(len(string)):
            self.assertEquals(scanner.next(), string[i])

    def test_match(self):
        """
        it matches one of multiple searchstrings correctly
        """
        string = "dies ist \n  ein Test"
        scanner = Scanner(string)
        self.assertTrue(scanner.matches("dies"))
        self.assertFalse(scanner.matches("das"))

    def test_end(self):
        """
        it recognizes the end of strings
        """
        string = "dies ist \n  ein Test"
        scanner = Scanner(string)
        for _ in xrange(len(string)):
            self.assertFalse(scanner.end())
            scanner.next()
        self.assertTrue(scanner.end())
        scanner.next()
        self.assertTrue(scanner.end())
        scanner.seek(2)
        self.assertFalse(scanner.end())

    def test_whitespace(self):
        """
        it skips whitespace
        """
        string = "   dies ist \n  ein Test"
        scanner = Scanner(string)
        self.assertFalse(scanner.matches("dies"))
        scanner.skip_whitespace()
        self.assertTrue(scanner.matches("dies"))

    def test_comment(self):
        """
        it skips comments
        """
        string = ";dies ist ein Kommentar \n Dies nicht mehr!"
        scanner = Scanner(string)
        self.assertFalse(scanner.matches("Dies nicht mehr!"))
        scanner.skip_comment()
        scanner.skip_whitespace()
        self.assertTrue(scanner.matches("Dies nicht mehr!"))


    def test_until(self):
        """
        it captures the substring to the next occurrence of a searched string
        """
        string = "   dies ist \n  ein Test"
        scanner = Scanner(string)
        scanner.skip_whitespace()
        self.assertFalse(scanner.matches("ist"))
        capture = scanner.until("ein", "ist", "Test")
        self.assertTrue(scanner.matches("ist"))
        self.assertEquals(capture, "dies ")

        self.assertRaises(UnexpectedEndOfStringException, scanner.until, "gibt es nicht")

    def test_consume(self):
        """
        it consumes substrings
        """
        string = "true false nil"
        scanner = Scanner(string)

        self.assertRaises(UnexpectedCharacterException, scanner.consume, "wurst")
        self.assertTrue(scanner.matches("true"))
        scanner.consume("true")
        self.assertFalse(scanner.matches("false"))
        scanner.skip_whitespace()
        self.assertTrue(scanner.matches("false"))
        scanner.consume("false")
        scanner.skip_whitespace()
        self.assertTrue(scanner.matches("nil"))
        scanner.consume("nil")

    def test_token(self):
        """
        it consumes a token
        """
        string = "a b c"
        scanner = Scanner(string)
        tok = scanner.token()
        self.assertEquals(tok, 'a')

        string = "tok"
        scanner = Scanner(string)
        tok = scanner.token()
        self.assertEquals('tok', tok)

    def test_string(self):
        """
        it consumes a string
        """

        string = '  \n " \n ; comment \n test\n "   '
        scanner = Scanner(string)
        scanner.skip_whitespace()
        tok = scanner.token()
        self.assertEquals('" \n ; comment \n test\n "', tok)

    def test_quote(self):
        """
        it recognizes quotes as separate tokens
        """

        tokens = tokenize("'a ;123 '(test")

        logging.info(tokens)

        self.assertEquals(["'", "a"], tokens)

if __name__ == '__main__':
    unittest.main()
