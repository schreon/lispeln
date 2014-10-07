import logging
from lispeln.evaluator.environment import Environment
from lispeln.scheme.constants import Nil, Integer, Float, Boolean
from lispeln.scheme.expressions import Symbol, Procedure, Pair
from lispeln.scheme.syntax import If, And, Or, Define, Set, Let, Lambda, Begin, Car, Cdr, Quote, Syntax


def eval_define(arguments, env):
    if len(arguments) != 2:
        raise Exception("define takes exactly 2 arguments: symbol and an expression")
    symbol = arguments[0]
    expression = arguments[1]
    env[symbol] = evaluate(expression, env)


def eval_set(arguments, env):
    if len(arguments) != 2:
        raise Exception("set! takes exactly 2 arguments: symbol and an expression")
    symbol = arguments[0]
    expression = arguments[1]
    if symbol not in env:
        raise Exception("Unknown Symbol %s" % str(symbol.value))
    env[symbol] = evaluate(expression, env)


def eval_let(arguments, env):
    if len(arguments) != 2:
        raise Exception("let takes exactly 2 arguments: list of bindings and an expression")
    bindings = arguments[0]
    expression = arguments[1]
    scope = Environment(env)
    for (symbol, value) in bindings:
        scope[symbol] = evaluate(value, scope)
    return evaluate(expression, scope)


def eval_constant(constant, env):
    return constant


def eval_cons(cons, env):
    return Pair(evaluate(cons.first, env), evaluate(cons.rest, env))


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


class LambdaImplementation(object):
    def __init__(self, parent, formals, body):
        self.parent = parent
        self.formals = formals
        self.body = body

    def __call__(self, *arguments):
        logging.info("Lambda --> implementation")

        # create a nested environment
        scope = Environment(self.parent)

        if len(arguments) != len(self.formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(self.formals)))

        # 1. update the scope depending on the positional values in the formals
        for symbol, value in zip(self.formals, arguments):
            scope[symbol] = evaluate(value, scope)

        # 2. evaluate the body
        operands = [evaluate(op, scope) for op in self.body]

        # return the last operand
        return operands[-1]

def eval_lambda(args, env, name=None):
    if len(args) < 2:
        raise Exception("Lambda expects at least 2 arguments: formals and at least one body element")

    formals = args[0]
    body = args[1:]

    implementation = LambdaImplementation(env, formals, body)

    return Procedure(implementation, num_args=len(formals), name=name)


def eval_and(arguments, env):
    res = Boolean(True)
    for arg in arguments:
        arg = evaluate(arg, env)
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res


def eval_or(arguments, env):
    res = Boolean(False)
    for arg in arguments:
        arg = evaluate(arg, env)
        if arg == Boolean(True):
            return Boolean(True)
        else:
            res = arg
    return res


def eval_if(arguments, env):
    if len(arguments) != 3:
        raise Exception("if takes exactly 3 arguments: test, consequent, alternate")
    test = arguments[0]
    consequent = arguments[1]
    alternate = arguments[2]
    if evaluate(test, env).value == True:
        return evaluate(consequent, env)
    else:
        return evaluate(alternate, env)


def eval_begin(arguments, environment):
    for expr in arguments[:-1]:
        evaluate(expr, environment)
    return evaluate(arguments[-1], environment)


def eval_car(expression, environment):
    return evaluate(expression.pair, environment).first


def eval_cdr(expression, environment):
    return evaluate(expression.pair, environment).rest


def eval_quote(arguments, _):
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
    Car: eval_car,
    Cdr: eval_cdr,
    Quote: eval_quote
}


def eval_list(l, environment):
    if len(l) < 1:
        return Nil()

    first = l[0]
    rest = l[1:]

    # if first is syntax, evaluate appropriately
    if isinstance(first, Syntax):
        eval_syntax = syntax[first.__class__]
        return eval_syntax(rest, environment)

    # else, evaluate first
    first = evaluate(first, environment)

    # if first is a procedure, call it
    if isinstance(first, Procedure):
        operands = [evaluate(operand, environment) for operand in rest]
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
}


def evaluate(expression, environment):
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Unknown expression: %s" % key.__name__)
    else:
        logging.info("Evaluate %s" % key.__name__)
        return eval_map[key](expression, environment)