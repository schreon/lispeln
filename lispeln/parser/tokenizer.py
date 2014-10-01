import logging
from lispeln.parser.scanner import Scanner
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil
from lispeln.scheme.derived import Let, Cons
from lispeln.scheme.environment import Symbol
from lispeln.scheme.logic import If, And
from lispeln.scheme.procedure import Lambda
import re



constants = {
    re.compile(r"^[0-9]+$"): Integer,
    re.compile(r"^[0-9]+.[0-9]+$"): Float,
    re.compile(r"false|true"): Boolean
}

syntax = {
    re.compile(r"^if$"): If,
    re.compile(r"^and$"): And,
    re.compile(r"^define$"): Define,
    re.compile(r"^set!$"): Set,
    re.compile(r"^let$"): Let,
    re.compile(r"^\'\(\)"): Nil,
    re.compile(r"^cons"): Cons,
    re.compile(r"^lambda$"): Lambda,
}

symbols = {
    re.compile(r"^(?!\#%)(\#)?\.?[^\s\(\)\[\]\{\}\"\,\'\;\#\|\\]+$"): Symbol
}


def match(string, dic):
    for pattern, cls in dic.iteritems():
        if pattern.match(string):
            return cls
    return None


def tokenize(code):
    logging.info("read")
    code = code.replace(r"\r\n", "\n")
    out = read(Scanner(code))
    if type(out) != list:
        out = [out]
    return out


def read(scanner):
    logging.info("read")

    scanner.skip_whitespace()
    next = scanner.peek()

    if next == '(':
        return read_list(scanner)
    else:
        return read_token(scanner)

def read_list(scanner):
    logging.info("read list")
    scanner.consume('(')
    scanner.skip_whitespace()

    _list = []
    while not scanner.end() and scanner.peek() != ')':
        _list.append(read(scanner))

    scanner.skip_whitespace()
    scanner.consume(')')
    return _list

def read_token(scanner):
    logging.info("read token")
    logging.info("remaining: %s" % scanner.string[scanner.cursor:])
    tok = scanner.token()
    logging.info("Read token %s" % tok)
    return tok
