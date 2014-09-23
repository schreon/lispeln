import unittest
from lispeln.reader import Reader, EndOfStringException, UnexpectedInputException


class ReaderTestCase(unittest.TestCase):
    def test_initialize(self):
        """
        it does initialize correctly
        """
        string = ""
        reader = Reader(string)
        self.assertIsNotNone(reader)

    def test_seek(self):
        """
        it does seek correctly
        """
        string = "dies ist \n  ein Test"
        reader = Reader(string)
        for i in xrange(len(string)):
            self.assertEquals(reader.seek(i), string[i])

    def test_peek(self):
        """
        it does peek correctly
        """
        string = "dies ist \n  ein Test"
        reader = Reader(string)
        for i in xrange(len(string)):
            self.assertEquals(reader.peek(i), string[i])

    def test_next(self):
        """
        it does traverse a string using the next method
        """
        string = "dies ist \n  ein Test"
        reader = Reader(string)
        for i in xrange(len(string)):
            self.assertEquals(reader.next(), string[i])

    def test_match(self):
        """
        it matches one of multiple searchstrings correctly
        """
        string = "dies ist \n  ein Test"
        reader = Reader(string)
        self.assertTrue(reader.matches("dies"))
        self.assertFalse(reader.matches("das"))

    def test_end(self):
        """
        it recognizes the end of strings
        """
        string = "dies ist \n  ein Test"
        reader = Reader(string)
        for _ in xrange(len(string)):
            self.assertFalse(reader.end())
            reader.next()
        self.assertTrue(reader.end())
        reader.next()
        self.assertTrue(reader.end())
        reader.seek(2)
        self.assertFalse(reader.end())

    def test_whitespace(self):
        """
        it skips whitespace
        """
        string = "   dies ist \n  ein Test"
        reader = Reader(string)
        self.assertFalse(reader.matches("dies"))
        reader.skip_whitespace()
        self.assertTrue(reader.matches("dies"))

    def test_comment(self):
        """
        it skips comments
        """
        string = ";dies ist ein Kommentar \n Dies nicht mehr!"
        reader = Reader(string)
        self.assertFalse(reader.matches("Dies nicht mehr!"))
        reader.skip_comment()
        reader.skip_whitespace()
        self.assertTrue(reader.matches("Dies nicht mehr!"))


    def test_until(self):
        """
        it captures the substring to the next occurrence of a searched string
        """
        string = "   dies ist \n  ein Test"
        reader = Reader(string)
        reader.skip_whitespace()
        self.assertFalse(reader.matches("ist"))
        capture = reader.until("ein", "ist", "Test")
        self.assertTrue(reader.matches("ist"))
        self.assertEquals(capture, "dies ")

        # should throw an EOS exception
        self.assertRaises(EndOfStringException, reader.until, "gibt es nicht")

    def test_consume(self):
        """
        it consumes substrings
        """
        string = "true false nil"
        reader = Reader(string)

        self.assertRaises(UnexpectedInputException, reader.consume, "wurst")
        self.assertTrue(reader.matches("true"))
        reader.consume("true")
        self.assertFalse(reader.matches("false"))
        reader.skip_whitespace()
        self.assertTrue(reader.matches("false"))
        reader.consume("false")
        reader.skip_whitespace()
        self.assertTrue(reader.matches("nil"))
        reader.consume("nil")

if __name__ == '__main__':
    unittest.main()
