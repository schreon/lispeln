import logging
from lispeln.evaluator.environment import Environment
from lispeln.scheme.constants import Nil, Integer, Float, Boolean, String
from lispeln.scheme.expressions import Symbol, Procedure, Pair
from lispeln.scheme.syntax import If, And, Or, Define, Set, Let, Lambda, Begin, Quote, Syntax


def eval_define(arguments, env, **kwargs):
    if len(arguments) != 2:
        raise Exception("define takes exactly 2 arguments: symbol and an expression")
    symbol = arguments[0]
    expression = arguments[1]
    logging.info("DEFINE: from_symbol=%s" % symbol.value)
    env[symbol] = evaluate(expression, env, from_symbol=symbol.value)


def eval_set(arguments, env, **kwargs):
    if len(arguments) != 2:
        raise Exception("set! takes exactly 2 arguments: symbol and an expression")
    symbol = arguments[0]
    expression = arguments[1]
    if symbol not in env:
        raise Exception("Unknown Symbol %s" % str(symbol.value))
    env[symbol] = evaluate(expression, env, **kwargs)


def eval_let(arguments, env, **kwargs):
    if len(arguments) != 2:
        raise Exception("let takes exactly 2 arguments: list of bindings and an expression")
    bindings = arguments[0]
    expression = arguments[1]
    scope = Environment(env)
    for (symbol, value) in bindings:
        scope[symbol] = evaluate(value, scope, **kwargs)
    return evaluate(expression, scope, **kwargs)


def eval_constant(constant, env, **kwargs):
    return constant


def eval_cons(cons, env, **kwargs):
    return Pair(evaluate(cons.first, env, **kwargs), evaluate(cons.rest, env, **kwargs))


def eval_symbol(symbol, env, **kwargs):
    if symbol not in env:
        raise Exception("Unbound identifier %s" % symbol.value)
    return evaluate(env[symbol], env, **kwargs)

def eval_procedure(proc, env, **kwargs):
    return proc


class LambdaImplementation(object):
    def __init__(self, parent, formals, body):
        self.parent = parent
        self.formals = formals
        self.body = body

    def __call__(self, *arguments, **kwargs):
        logging.info("Lambda --> implementation")

        # create a nested environment
        scope = Environment(self.parent)

        if len(arguments) != len(self.formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(self.formals)))

        for symbol, value in zip(self.formals, arguments): # 1. update the scope depending on the positional values in the formals
            scope[symbol] = evaluate(value, scope, **kwargs)

        # 2. evaluate the body
        operands = [evaluate(op, scope, **kwargs) for op in self.body]

        # return the last operand
        return operands[-1]

def eval_lambda(args, env, from_symbol=None, **kwargs):
    logging.info("LAMBDA: from_symbol=%s" % from_symbol)
    if len(args) < 2:
        raise Exception("Lambda expects at least 2 arguments: formals and at least one body element")

    formals = args[0]
    body = args[1:]
    implementation = LambdaImplementation(env, formals, body)

    return Procedure(implementation, num_args=len(formals), name=from_symbol)


def eval_and(arguments, env, **kwargs):
    res = Boolean(True)
    for arg in arguments:
        arg = evaluate(arg, env, **kwargs)
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res


def eval_or(arguments, env, **kwargs):
    res = Boolean(False)
    for arg in arguments:
        arg = evaluate(arg, env, **kwargs)
        if arg == Boolean(True):
            return Boolean(True)
        else:
            res = arg
    return res


def eval_if(arguments, env, **kwargs):
    if len(arguments) != 3:
        raise Exception("if takes exactly 3 arguments: test, consequent, alternate")
    test = arguments[0]
    consequent = arguments[1]
    alternate = arguments[2]
    if evaluate(test, env, **kwargs).value == True:
        return evaluate(consequent, env, **kwargs)
    else:
        return evaluate(alternate, env, **kwargs)


def eval_begin(arguments, environment, **kwargs):
    for expr in arguments[:-1]:
        evaluate(expr, environment, **kwargs)
    return evaluate(arguments[-1], environment, **kwargs)

def eval_quote(arguments, _, **kwargs):
    if len(arguments) != 1:
        raise Exception("Quote takes exactly 1 argument")
    return arguments[0]


syntax = {
    If: eval_if,
    And: eval_and,
    Or: eval_or,
    Define: eval_define,
    Set: eval_set,
    Let: eval_let,
    Lambda: eval_lambda,
    Begin: eval_begin,
    Quote: eval_quote
}


def eval_list(l, environment, **kwargs):
    first = l[0]
    rest = l[1:]

    # if first is syntax, evaluate appropriately
    if isinstance(first, Syntax):
        eval_syntax = syntax[first.__class__]
        return eval_syntax(rest, environment, **kwargs)

    # else, evaluate first
    first = evaluate(first, environment, **kwargs)

    # if first is a procedure, call it
    if isinstance(first, Procedure):
        operands = [evaluate(operand, environment, **kwargs) for operand in rest]
        return first(*operands)

    raise Exception("Could not evaluate list: %s" % repr(l))


eval_map = {
    list: eval_list,
    Procedure: eval_procedure,
    Pair: eval_cons,
    Symbol: eval_symbol,
    Nil: eval_constant,
    Integer: eval_constant,
    Float: eval_constant,
    Boolean: eval_constant,
    String: eval_constant
}


def evaluate(expression, environment, **kwargs):
    if "from_symbol" in kwargs:
        logging.info("EVALUATE: from_symbol=%s" % kwargs['from_symbol'])
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Unknown expression: %s" % key.__name__)
    else:
        logging.info("Evaluate %s" % key.__name__)
        return eval_map[key](expression, environment, **kwargs)