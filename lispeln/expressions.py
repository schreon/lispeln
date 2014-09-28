from lispeln.environment import Environment


class Expression(object):
    def eval(self, environment):
        raise Exception("Expression not implemented.")

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.value)

    def __str__(self):
        return str(self.value)

class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def eval(self, environment):
        """
        Contants evaluate to themselves
        """
        return self


class SingletonByValue(type):
    """
    Metaclass designed for Symbols. For each Symbol value there is only one Symbol instance.
    """
    _instances = {}
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, cls):  # if the value is of the same type, just return the value
            return value

        if value not in cls._instances.keys():
            cls._instances[value] = super(SingletonByValue, cls).__call__(value, *args, **kwargs)
        return cls._instances[value]

class Symbol(Expression):
    __metaclass__ = SingletonByValue

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "'%s" % self.value

class Procedure(Expression):

    def __init__(self, name, operand, *args):
        self.name = name
        self.operand = operand
        self.args = args

    def eval(self, environment):
        """
        Calls the operand with the arguments
        """
        # evaluate the arguments with the given scope
        args = [arg.eval(environment) for arg in self.args]
        # call the operand with the arguments
        return self.operand(*args)

class Call(Expression):
    def __init__(self, *expressions):
        super(Expression, self).__init__()
        self.expressions = expressions

    def eval(self, environment):
        """
        Calls a procedure
        """
        scope = Environment(environment)
        proc = self.expressions[0]
        return proc.eval(scope)


