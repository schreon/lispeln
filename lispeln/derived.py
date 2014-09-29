from lispeln.constants import Nil
from lispeln.expressions import Expression, Environment


class Cons(Expression):
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def ravel(self):

        """
        Returns this cons as a flat python list.
        :return:
        """
        if not isinstance(self.rest, Cons):
            return [self.first, self.rest]
        else:
            last = self.rest
            l = [self.first]
            while isinstance(last, Cons):
                l.append(last.first)
                last = last.rest
            l.append(last)
            return l

    def __str__(self):
        if isinstance(self.rest, Cons):
            l = self.ravel()
            res = "(" + " ".join([str(el) for el in l[:-1]])
            if isinstance(l[-1], Nil):
                res += ")"
            else:
                res += " . "+str(l[-1])+")"

            return res

        if isinstance(self.rest, Nil):
            return "(%s)" % self.first

        return "(%s . %s)" % (self.first, self.rest)

    def __repr__(self):
        return "<%s: (%s.%s)>" % (self.__class__.__name__, self.first, self.rest)

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