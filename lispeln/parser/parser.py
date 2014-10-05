import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil, Constant, String
from lispeln.scheme.derived import Let, Pair, Begin, Car, Cdr
from lispeln.scheme.expression import Expression, Quote
from lispeln.scheme.logic import If, And, Or
from lispeln.scheme.procedure import Lambda, Call
from lispeln.scheme.symbol import Symbol
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
    return Begin(*[_parse(item) for item in rest])


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

def _parse_let(items):
    bindings, expression = items

    bindings = [(_parse(symbol), _parse(value)) for (symbol, value) in bindings]
    expression = _parse(expression)

    logging.info("Parse Let %s -> %s" % (repr(bindings), repr(expression)))
    return Let(bindings, expression)

def _parse_and(expressions):
     return And(*[_parse(expr) for expr in expressions])

def _parse_or(expressions):
    return Or(*[_parse(expr) for expr in expressions])

def _parse_if(expressions):
    return If(*[_parse(expr) for expr in expressions])

def _parse_quote(expressions):
    logging.info("parse quote on expressions %s" % expressions)
    return Quote(*[_parse(expr) for expr in expressions])

syntax = {
    'begin': _parse_begin,
    'define': _parse_define,
    'set!': _parse_set,
    'lambda': _parse_lambda,
    'let': _parse_let,
    'and': _parse_and,
    'or': _parse_or,
    'if': _parse_if,
    "'": _parse_quote,
    "quote": _parse_quote
}

def _parse_token(tok):
    logging.info("parse token: %s" % tok)
    # Constant > Syntax > Symbol
    const_parse = match(tok, constants)
    if const_parse is not None:
        return const_parse(tok)

    if tok in syntax:
        return tok

    if match(tok, symbols) is not None:
        return Symbol(tok)

    if tok[0] == '"':
        return String(tok[1:-1])  # omit the quotation marks

    raise Exception("Token cannot be matched: %s" % tok)


def _parse_list(_list):
    if len(_list) < 1:
        logging.info("_parse_list: Nil")
        return Nil()

    first = _parse(_list[0])

    # if the first argument is a constant, just return the list
    if isinstance(first, Constant):
        logging.info("_parse_list: constant list")
        return [_parse(item) for item in _list]

    # if the first argument is syntax, create a syntax object from this
    if first in syntax:
        logging.info("_parse_list: syntax %s" % first)
        return syntax[first](_list[1:])

    #else, it must be a symbol and this is a call
    logging.info("_parse_list: call")
    return _parse_call(_list)


def _parse(item):
    if type(item) == list:
        logging.info("_parse: it is a list: %s" % item)
        return _parse_list(item)
    else:
        logging.info("_parse: it is a token: %s" % item)
        return _parse_token(item)