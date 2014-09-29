import logging
from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Integer, Float, Boolean
from lispeln.scheme.derived import Let, Cons
from lispeln.scheme.environment import Environment, Symbol
from lispeln.scheme.procedure import Lambda, Call, Procedure


def eval_define(self, env):
    env[self.symbol] = self.expression.eval(env)


def eval_set(self, env):
    if self.symbol not in env:
        raise Exception("Unknown Symbol %s" % str(self.symbol))
    env[self.symbol] = self.expression.eval(env)


def eval_constant(self, environment):
    """
    Contants evaluate to themselves
    """
    return self


def eval_let(self, env):
    scope = Environment(env)
    for (symbol, value) in self.definitions:
        scope[symbol] = value
    return self.expression.eval(scope)


def eval_begin(self, environment):
    for expr in self.expressions[:-1]:
        expr.eval(environment)
    return self.expressions[-1].eval(environment)


def eval_symbol(self, environment):
    if isinstance(environment[self], Lambda):
        return evaluate(environment[self], environment, name=self.value)
    else:
        return evaluate(environment[self], environment)


def eval_quote(self, env):
    return self.expression


def eval_if(self, env):
    if self.test.eval(env).value == True:
        return self.consequent.eval(env)
    else:
        return self.alternate.eval(env)


def eval_and(self, env):
    res = Boolean(True)
    for arg in self.args:
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res.eval(env)


def eval_procedure(self, environment):
    return self


def eval_call(self, environment):
    """
    Calls a procedure
    """
    operator = self.operator.eval(environment)
    operands = [operand.eval(environment) for operand in self.operands]
    return operator(*operands)


def eval_lambda(self, environment, name=None):
    super(Lambda, self).eval()
    scope = Environment(environment)

    this = self

    def implementation(*arguments):
        if len(arguments) != len(this.formals):
            raise Exception("Invalid number of Arguments: %d, Expected: %d" % (len(arguments), len(this.formals)))
        for symbol, value in zip(this.formals, arguments):
            scope[symbol] = value.eval(scope)
        operator = this.body[0]
        operands = [op.eval(scope) for op in this.body[1:]]
        return Call(operator, *operands).eval(scope)

    logging.info("Evaluating Lambda with name: %s" % str(name))
    return Procedure(implementation, num_args=len(self.formals), name=name)


def eval_cons(self, environment, *args, **kwargs):
    return Cons(evaluate(self.first, environment, *args, **kwargs), evaluate(self.rest, environment, *args, **kwargs))


eval_map = {
    Define: eval_define,
    Set: eval_set,
    Let: eval_let,
    Integer: eval_constant,
    Float: eval_constant,
    Boolean: eval_constant,
    Cons: eval_cons,
    Symbol: eval_symbol
}


def evaluate(expression, environment, *args, **kwargs):
    key = expression.__class__
    if key not in eval_map:
        raise Exception("Can't evaluate expression of type: %s" % str(key))
    else:
        return eval_map[key](expression, environment, *args, **kwargs)