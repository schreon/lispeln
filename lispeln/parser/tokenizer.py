import logging
from lispeln.parser.scanner import Scanner

def tokenize(code):
    logging.info("read")
    code = code.replace(r"\r\n", "\n")
    return read(Scanner(code))


def read(scanner):
    logging.info("read")

    scanner.skip_whitespace()

    next = scanner.peek()

    if next == '(':
        return read_list(scanner)
    elif next == ';':
        scanner.skip_comment()
        return read(scanner)
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
