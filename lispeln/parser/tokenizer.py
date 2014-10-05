import logging
from lispeln.parser.scanner import Scanner

def tokenize(code):
    logging.info("tokenize")
    code = code.replace(r"\r\n", "\n")
    scanner = Scanner(code)
    return read(scanner)


def read(scanner):
    logging.info("read")

    scanner.skip_whitespace()

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
    tok = scanner.token()
    logging.info("read token %s" % tok)
    return tok

def read_quote(scanner):
    logging.info("read quote")
    scanner.consume("'")
    res = ["'"]

    res.append(read(scanner))

    return res