from lispeln.scheme.constants import Nil
from lispeln.scheme.expressions import Expression, Environment


class Cons(Expression):
    def __init__(self, first, rest, *args, **kwargs):
        super(Cons, self).__init__(*args, **kwargs)
        self.first = first
        self.rest = rest

    def eval(self, environment):
        return Cons(self.first.eval(environment), self.rest.eval(environment))

class Let(Expression):
    def __init__(self, definitions, expression):
        super(Let, self).__init__()
        self.definitions = definitions
        self.expression = expression

    def eval(self, env):
        scope = Environment(env)
        for (symbol, value) in self.definitions:
            scope[symbol] = value
        return self.expression.eval(scope)

class Begin(Expression):
    def __init__(self, *expressions):
        super(Begin, self).__init__()
        self.expressions = expressions

    def eval(self, environment):
        for expr in self.expressions[:-1]:
            expr.eval(environment)
        return self.expressions[-1].eval(environment)