import logging
from lispeln.parser.scanner import Scanner

def tokenize(code):
    code = code.replace(r"\r\n", "\n")
    scanner = Scanner(code)
    exprs = []
    while not scanner.end():
        r = read(scanner)
        if r is not None:
            exprs.append(r)
    return exprs


def read(scanner):
    scanner.skip_whitespace()

    if scanner.end():
        return None

    next = scanner.peek()

    if next == '(':
        return read_list(scanner)
    elif next == ';':
        scanner.skip_comment()
        return read(scanner)
    elif next == "'":
        return read_quote(scanner)
    else:
        return read_token(scanner)


def read_list(scanner):
    scanner.consume('(')
    scanner.skip_whitespace()

    _list = []
    while not scanner.end() and scanner.peek() != ')':
        _list.append(read(scanner))

    scanner.skip_whitespace()
    scanner.consume(')')
    scanner.skip_whitespace()
    return _list

def read_token(scanner):
    tok = scanner.token()
    scanner.skip_whitespace()
    return tok

def read_quote(scanner):
    scanner.consume("'")
    res = ["'"]
    scanner.skip_whitespace()
    res.append(read(scanner))

    return res