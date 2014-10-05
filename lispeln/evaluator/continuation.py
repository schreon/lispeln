import logging

from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean
from lispeln.scheme.derived import Let, Cons
from lispeln.evaluator.environment import Environment
from lispeln.scheme.procedure import Lambda, Call, Procedure
from lispeln.scheme.symbol import Symbol


def eval_define(self, env):
    logging.info("eval_define")
    env[self.symbol] = self.expression.eval(env)


def eval_set(self, env):
    logging.info("eval_set")
    if self.symbol not in env:
        raise Exception("Unknown Symbol %s" % str(self.symbol))
    env[self.symbol] = self.expression.eval(env)


def eval_let(self, env):
    logging.info("eval_let")
    scope = Environment(env)
    for (symbol, value) in self.definitions:
        scope[symbol] = value
    return self.expression.eval(scope)


def eval_begin(self, environment):
    logging.info("eval_begin")
    for expr in self.expressions[:-1]:
        expr.eval(environment)
    return self.expressions[-1].eval(environment)



def eval_quote(self, env):
    logging.info("eval_quote")
    return self.expression


def eval_if(self, env):
    logging.info("eval_if")
    if self.test.eval(env).value == True:
        return evaluate(self.consequent, env)
    else:
        return evaluate(self.alternate, env)


def eval_and(self, env):
    logging.info("eval_and")
    res = Boolean(True)
    for arg in self.args:
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res.eval(env)


def eval_cons(self, environment, *args, **kwargs):
    logging.info("eval_cons")
    return Cons(evaluate(self.first, environment, *args, **kwargs), evaluate(self.rest, environment, *args, **kwargs))

def eval_lambda(self, environment, name=None):
    logging.info("EVAL: lambda")
    logging.info("Evaluating Lambda with name: %s" % str(name))

    # create a nested environment
    scope = Environment(environment)

    def implementation(*arguments):
        logging.info("Lambda --> implementation")

        # 1. evaluate the operands depending on the current situation
        formals = self.formals
        operator = evaluate(self.body[0], scope)
        operands = [evaluate(op, scope) for op in self.body[1:]]

        if len(arguments) != len(formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(self.formals)))

        # 2. update the scope depending on the positional values in the formals
        for symbol, value in zip(formals, arguments):
            scope[symbol] = evaluate(value, scope)


        # promise the execution
        dependencies = operands + formals + [operator]
        def do():
            operator(*operands)

        promise = Promise(do, dependencies)

        # execute the operator
        return promise

    def ready():
        Procedure(implementation, num_args=len(self.formals), name=name)
    return Promise(ready, )

def eval_procedure(proc, environment):
    logging.info("EVAL: procedure")

    return (proc

def eval_constant(promise, constant, environment):
    logging.info("eval_constant: %s" % constant.__class__.__name__)
    return constant, environment

def eval_symbol(promise, symbol, environment):
    logging.info("EVAL: symbol")
    if isinstance(environment[symbol], Lambda):
        name = symbol.value
    else:
        name = None
    promise.then(evaluate, environment[symbol], environment, name=name)

def eval_call(promise, call, environment, **kwargs):
    logging.info("EVAL: call")

    operands = [evaluate(promise, operand, environment) for operand in call.operands]
    operator = evaluate(promise, call.operator, environment)

    promise.then(operator, *operands)

class Promise(object):
    def __init__(self):
        self.heap = []

    def resolve(self, *args):
        for func in self.heap:
            logging.info("Resolving '%s'" % func.__class__.__name__)
            args = func(self, *args)

    def then(self, func):
        logging.info("Adding '%s'" % func.__class__.__name__)
        self.heap.append(func)
        return self

    def __repr__(self):
        return "Promise:%s" % self.func.__name__

    def __str__(self):
        raise Exception("Can't print a Promise")

eval_map = {
    Define: eval_define,
    Set: eval_set,
    Let: eval_let,
    Integer: eval_constant,
    Float: eval_constant,
    Boolean: eval_constant,
    Cons: eval_cons,
    Symbol: eval_symbol,
    Call: eval_call,
    Procedure: eval_procedure,
    Lambda: eval_lambda
}

def evaluate(promise, expression, environment, **kwargs):
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Can't evaluate expression of type: %s" % str(key))
    else:
        func = eval_map[key]
        if promise is None:
            promise = Promise()
        return func(promise, expression, environment, **kwargs)
        #return promise.then(func, expression, environment, **kwargs)