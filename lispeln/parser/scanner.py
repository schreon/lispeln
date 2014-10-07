WHITESPACE = frozenset([' ', '\n', '\t'])
TOKEN_END = frozenset([' ', '\n', '\t', ')'])

import logging

class UnexpectedCharacterException(Exception):
    pass


class UnexpectedEndOfStringException(Exception):
    pass


class Scanner(object):
    def __init__(self, string):
        self.string = string
        self.cursor = 0

    def seek(self, position):

        """

        :param position: the position to seek to
        """
        self.cursor = position
        return self.string[self.cursor]

    def peek(self, offset=0):
        """

        :param offset:
        :return: the character at the given position relative to the current cursor
        """
        return self.string[self.cursor + offset]

    def next(self):

        """


        :return: the character at the current position and move cursor by 1
        """
        if self.cursor < len(self.string):
            s = self.string[self.cursor]
            self.cursor += 1
            return s
        else:
            return None

    def matches(self, *strings):
        """
        If the one of the given strings matches the string at the current position, return true

        :param strings strings to search
        :return: True if the strings match, False if not
        """
        for string in strings:
            l = len(string)
            if self.string[self.cursor:self.cursor + l] == string:
                return True
        return False

    def end(self):
        if self.cursor < len(self.string):
            return False
        else:
            return True

    def skip_whitespace(self):
        """
        Move cursor to the next non-whitespace character
        """
        while not self.end() and self.matches(*WHITESPACE):
            self.next()

    def skip_comment(self):
        """
        Skip comment until linebreak
        """
        if self.peek() == ';':
            while not self.end() or self.matches('\n'):
                self.next()

    def read_string(self):
        self.consume('"')

        start = self.cursor
        while not self.end() and not self.peek(0) == '"':
            self.next()
        self.consume('"')
        return '"' + self.string[start:self.cursor]

    def token(self):
        """
        Reads until the next valid token end (can also be the end of string).
        :return: the next token
        """
        # string?
        if self.peek(0) == '"':
            return self.read_string()

        start = self.cursor
        while not self.end():
            for string in TOKEN_END:
                if self.matches(string):
                    return self.string[start:self.cursor]
            self.next()
        return self.string[start:self.cursor]

    def consume(self, *strings):
        """
        Tries to consume one of the given strings. If none of them matches, an UnexpectedInputException is raised.
        :param strings: one of these strings must match.
        """
        for string in strings:
            if self.matches(string):
                self.cursor += len(string)
                return True

        raise UnexpectedCharacterException(
            "Expected one of: " + str(strings) + ", instead found: " + self.string[self.cursor:])
