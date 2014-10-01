import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean, Nil
from lispeln.scheme.derived import Let, Cons
from lispeln.scheme.environment import Symbol, Environment
from lispeln.scheme.logic import And, If
from lispeln.scheme.procedure import Call, Procedure, Lambda


def eval_define(define, env):
    env[define.symbol] = evaluate(define.expression, env)

def eval_set(_set, env):
    if _set.symbol not in env:
        raise Exception("Unknown Symbol %s" % str(_set.symbol.value))
    env[_set.symbol] = evaluate(_set.expression, env)

def eval_let(let, env):
    raise Exception("not implemented yet")

def eval_constant(constant, env):
    return constant

def eval_cons(cons, env):
    return Cons(evaluate(cons.first, env), evaluate(cons.rest, env))

def eval_symbol(symbol, env):
    if symbol not in env:
        raise Exception("Unbound identifier %s" % symbol.value)
    value = env[symbol]
    if isinstance(value, Lambda):
        return eval_lambda(value, env, name=symbol.value)
    else:
        return evaluate(value, env)

def eval_call(call, env):
    operands = [evaluate(operand, env) for operand in call.operands]
    operator = evaluate(call.operator, env)

    return operator(*operands)

def eval_procedure(proc, env):
    return proc

def eval_lambda(_lambda, env, name=None):
    # create a nested environment
    scope = Environment(env)

    def implementation(*arguments):
        logging.info("Lambda --> implementation")

        formals = _lambda.formals

        if len(arguments) != len(formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(_lambda.formals)))

        # 1. update the scope depending on the positional values in the formals
        for symbol, value in zip(formals, arguments):
            scope[symbol] = evaluate(value, env)

        # 2. evaluate the operands depending on the current situation
        operator = evaluate(_lambda.body[0], scope)
        operands = [evaluate(op, scope) for op in _lambda.body[1:]]

        # execute the operator
        return operator(*operands)

    return Procedure(implementation, num_args=len(_lambda.formals), name=name)

def eval_and(_and, env):
    res = Boolean(True)
    for arg in _and.args:
        arg = evaluate(arg, env)
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res

def eval_if(_if, env):
    if evaluate(_if.test, env).value == True:
        return evaluate(_if.consequent, env)
    else:
        return evaluate(_if.alternate, env)

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
        logging.info("Evaluate %s" % key.__name__)
        return eval_map[key](expression, environment)