import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean
from lispeln.scheme.derived import Let, Cons
from lispeln.scheme.environment import Environment, Symbol
from lispeln.scheme.procedure import Lambda, Call, Procedure


def eval_define(self, env):
    logging.info("eval_define")
    env[self.symbol] = self.expression.eval(env)


def eval_set(self, env):
    logging.info("eval_set")
    if self.symbol not in env:
        raise Exception("Unknown Symbol %s" % str(self.symbol))
    env[self.symbol] = self.expression.eval(env)

def eval_constant(self, environment):
    logging.info("eval_constant: %s" % self.__class__.__name__)
    return self


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


def eval_symbol(self, environment):
    logging.info("eval_symbol")
    if isinstance(environment[self], Lambda):
        return evaluate(environment[self], environment, name=self.value)
    else:
        return evaluate(environment[self], environment)


def eval_quote(self, env):
    logging.info("eval_quote")
    return self.expression


def eval_if(self, env):
    logging.info("eval_if")
    if self.test.eval(env).value == True:
        return self.consequent.eval(env)
    else:
        return self.alternate.eval(env)


def eval_and(self, env):
    logging.info("eval_and")
    res = Boolean(True)
    for arg in self.args:
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res.eval(env)


def eval_procedure(self, environment):
    logging.info("eval_procedure")
    return self

def eval_lambda(self, environment, name=None):
    logging.info("eval_lambda")
    scope = Environment(environment)

    this = self

    def implementation(*arguments):
        if len(arguments) != len(this.formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(this.formals)))
        for symbol, value in zip(this.formals, arguments):
            scope[symbol] = evaluate(value, scope)
        operator = this.body[0]
        operands = [evaluate(op, scope) for op in this.body[1:]]
        return evaluate(Call(operator, *operands), scope)

    logging.info("Evaluating Lambda with name: %s" % str(name))
    return Procedure(implementation, num_args=len(self.formals), name=name)


def eval_cons(self, environment, *args, **kwargs):
    logging.info("eval_cons")
    return Cons(evaluate(self.first, environment, *args, **kwargs), evaluate(self.rest, environment, *args, **kwargs))



def eval_call(self, environment):
    operands = [evaluate(operand, environment) for operand in self.operands]
    operator = evaluate(self.operator, environment)

    promise = Promise(lambda : operator(*operands), dependencies=operands+[operator])
    return promise


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

class Promise(object):
    promises = []
    def __init__(self, func, dependencies, *args, **kwargs):
        logging.info("New Promise %s" % func.__name__)
        self._resolving = False
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.dependencies = dependencies
        Promise.promises.append(self)

    def resolve(self):
        logging.info("Resolve promise %s" % self.func.__name__)
        res = self.func(*self.args, **self.kwargs)
        # if res is a list,
        # the following lines "pull" the result into this instance (without breaking outside references!)
        self.__dict__ = res.__dict__
        self.__class__ = res.__class__

    def __repr__(self):
        return "Promise:%s" % self.func.__name__

def resolve():
    iterations = 0
    while True:
        iterations += 1
        if len(Promise.promises) <= 0:
            break
        promise = Promise.promises.pop(0)
        if not isinstance(promise, Promise):
            logging.info("Promise already resolved")
            continue

        deps = 0
        if promise.dependencies is not None:
            for dep in promise.dependencies:
                if isinstance(dep, Promise):
                    Promise.promises.insert(0, dep)
                    deps += 1
        if deps > 0:
            Promise.promises.append(promise)
        else:
            promise.resolve()

        if isinstance(promise, Promise):
            Promise.promises.append(promise)

    logging.info("Needed %d iterations for resolving all promises" % iterations)

def evaluate(expression, *args, **kwargs):
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Can't evaluate expression of type: %s" % str(key))
    else:
        func = eval_map[key]
        return Promise(func, None, expression, *args, **kwargs)