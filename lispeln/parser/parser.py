import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil, Constant
from lispeln.scheme.derived import Let, Cons, Begin
from lispeln.scheme.environment import Symbol
from lispeln.scheme.expression import Expression
from lispeln.scheme.logic import If, And
from lispeln.scheme.procedure import Lambda, Call
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


def match(string, dic):
    for pattern, cls in dic.iteritems():
        if pattern.match(string):
            return cls
    return None

def parse(item):
    return _parse(item)

def _parse_lambda(rest):
    formals = rest[0]
    if type(formals) != list:
        raise Exception("Formals must be a list.")
    body = rest[1:]
    if type(body) != list:
        raise Exception("Body must be a list.")

    formals = [_parse(item) for item in formals]
    body = [_parse(item) for item in body]

    logging.info("Parse Lambda: formals %s" % repr(formals))
    logging.info("Parse Lambda: body %s" % repr(body))
    return Lambda(formals, *body)

def _parse_define(rest):
    symbol = _parse(rest[0])
    expression = _parse(rest[1])

    return Define(symbol, expression)

def _parse_begin(rest):
    logging.info("Parse Begin.")
    return Begin(_parse(item) for item in rest)


def _parse_set(rest):
    symbol, expression = rest
    symbol = _parse(symbol)
    expression = _parse(expression)
    logging.info("Parse Set: %s -> %s" % (repr(symbol), repr(expression)))
    return Set(symbol, expression)


def _parse_call(items):
    operator = _parse(items[0])
    operands = [_parse(item) for item in items[1:]]
    logging.info("Parse Call %s -> %s" % (repr(operator), repr(operands)))
    return Call(operator, *operands)


syntax = {
    'begin': _parse_begin,
    'define': _parse_define,
    'set!': _parse_set,
    'lambda': _parse_lambda,
}

def _parse_token(tok):
    # Constant > Syntax > Symbol
    const_parse = match(tok, constants)
    if const_parse is not None:
        return const_parse(tok)

    if tok in syntax:
        return tok

    if match(tok, symbols) is not None:
        return Symbol(tok)

    raise Exception("Token cannot be matched: %s" % tok)


def _parse_list(_list):
    first = _parse(_list[0])

    # if the first argument is a constant, just return the list
    if isinstance(first, Constant):
        return [_parse(item) for item in _list]

    if isinstance(first, str):
        if first == 'lambda':
            return _parse_lambda(_list[1:])

        if first == 'begin':
            return _parse_begin(_list[1:])

        if first == 'define':
            return _parse_define(_list[1:])

        if first == 'set!':
            return _parse_set(_list[1:])

        raise Exception("Cannot parse Syntax: %s" % repr(first))

    # if the first argument is syntax, create a syntax object from this, else, it must be a symbol and this is a call
    return _parse_call(_list)


def _parse(item):
    if type(item) == list:
        return _parse_list(item)
    else:
        return _parse_token(item)