import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil
from lispeln.scheme.derived import Let, Cons
from lispeln.scheme.environment import Symbol
from lispeln.scheme.logic import And, If
from lispeln.scheme.procedure import Call, Procedure, Lambda


def eval_define(define, env):
    raise Exception("not implemented yet")

def eval_set(_set, env):
    raise Exception("not implemented yet")

def eval_let(let, env):
    raise Exception("not implemented yet")

def eval_constant(constant, env):
    return constant

def eval_cons(cons, env):
    logging.info("evaluate cons")
    return Cons(evaluate(cons.first, env), evaluate(cons.rest, env))

def eval_symbol(symbol, env):
    if symbol not in env:
        raise Exception("Unbound identifier %s" % symbol.value)
    return env[symbol]

def eval_call(call, env):
    raise Exception("not implemented yet")

def eval_procedure(proc, env):
    raise Exception("not implemented yet")

def eval_lambda(_lambda, env):
    raise Exception("not implemented yet")

def eval_and(_and, env):
    raise Exception("not implemented yet")

def eval_if(_if, env):
    raise Exception("not implemented yet")

eval_map = {
    If: eval_if,
    And: eval_and,
    Define: eval_define,
    Set: eval_set,
    Let: eval_let,
    Nil: eval_constant,
    Integer: eval_constant,
    Float: eval_constant,
    Boolean: eval_constant,
    Cons: eval_cons,
    Symbol: eval_symbol,
    Call: eval_call,
    Procedure: eval_procedure,
    Lambda: eval_lambda,
}

def evaluate(expression, environment):
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Unknown expression: %s" % key.__name__)
    else:
        return eval_map[key](expression, environment)