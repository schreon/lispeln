import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil, Constant
from lispeln.scheme.derived import Let, Cons, Begin
from lispeln.scheme.environment import Symbol
from lispeln.scheme.logic import If, And
from lispeln.scheme.procedure import Lambda, Call
import re


def _parse_int(tok):
    return Integer(int(tok))

def _parse_float(tok):
    return Float(float(tok))

def _parse_boolean(tok):
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

syntax = {
    re.compile(r"^if$"): If,
    re.compile(r"^begin$"): Begin,
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

def parse(item):
    return _parse(item)

def _parse(item):
    if type(item) == list:
        logging.info("yeah, a list")
        return _parse_list(item)
    else:
        logging.info("yeah, a token: %s" % item)
        return _parse_token(item)

def _parse_list(_list):
    _list = [_parse(item) for item in _list]
    first = _list[0]
    rest = _list[1:]
    # if the first argument is a constant, just return the list
    if isinstance(first, Constant):
        return _list
    # if the first argument is syntax, create a syntax object from this, else, it must be a symbol and this is a call
    if isinstance(first, Symbol):
        return Call(*_list)
    else:
        return first(*rest)


def _parse_token(tok):
    # Constant > Syntax > Symbol
    if match(tok, constants) is not None:
        return match(tok, constants)(tok)

    if match(tok, syntax):
        return match(tok, syntax)

    if match(tok, symbols):
        return match(tok, symbols)(tok)

    raise Exception("Token cannot be matched: %s" % tok)