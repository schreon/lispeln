import logging
from lispeln.scheme.constants import Integer, Float, Boolean, String, Nil
from lispeln.scheme.expressions import Symbol
from lispeln.scheme.syntax import Begin, Define, Set, Lambda, Let, And, Or, If, Quote
import re


def _parse_int(tok):
    logging.info("Parse Integer %s" % tok)
    return Integer(int(tok))


def _parse_float(tok):
    logging.info("Parse Float %s" % tok)
    return Float(float(tok))


def _parse_boolean(tok):
    logging.info("Parse Boolean %s" % tok)
    if tok in ['true', '#t']:
        return Boolean(True)
    if tok in ['false', '#f']:
        return Boolean(False)
    raise Exception("Invalid Boolean: %s" % tok)


constants = {
    re.compile(r"^[0-9]+$"): _parse_int,
    re.compile(r"^[0-9]+.[0-9]+$"): _parse_float,
    re.compile(r"false|true|#f|#t"): _parse_boolean
}

symbols = {
    re.compile(r"^(?!\#%)(\#)?\.?[^\s\(\)\[\]\{\}\"\,\'\;\#\|\\]+$"): Symbol
}

syntax = {
    'begin': Begin,
    'define': Define,
    'set!': Set,
    'lambda': Lambda,
    'let': Let,
    'and': And,
    'or': Or,
    'if': If,
    "'": Quote,
    "quote": Quote
}


def match(string, dic):
    for pattern, cls in dic.iteritems():
        if pattern.match(string):
            return cls
    return None


def parse(item):
    return _parse(item)


def _parse(item):
    if type(item) == list:
        logging.info("_parse: it is a list: %s" % item)
        return _parse_list(item)
    else:
        logging.info("_parse: it is a token: %s" % item)
        return _parse_token(item)


def _parse_list(_list):
    if len(_list) < 1:
        logging.info("_parse_list: Nil")
        return Nil()

    return [_parse(item) for item in _list]


def _parse_token(tok):
    # Constant > Syntax > Symbol
    const_parse = match(tok, constants)
    if const_parse is not None:
        logging.info("parse constant: %s" % tok)
        return const_parse(tok)

    if tok in syntax:
        logging.info("parse syntax: %s" % tok)
        return syntax[tok]()

    if match(tok, symbols) is not None:
        logging.info("parse symbol: %s" % tok)
        return Symbol(tok)

    if tok[0] == '"':
        logging.info("parse string: %s" % tok)
        return String(tok[1:-1])  # omit the quotation marks

    raise Exception("Token cannot be matched: %s" % tok)
