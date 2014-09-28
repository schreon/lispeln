import collections

class Expression(object):
    def __init__(self, *args, **kwargs):
        pass

    def eval(self, *args, **kwargs):
        pass

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.value)

    def __str__(self):
        return str(self.value)


class Procedure(object):

    def __init__(self, implementation, num_args=None):
        super(Procedure, self).__init__()
        self.implementation = implementation
        self.num_args = num_args

    def __call__(self, *arguments):
        """
        Calls the implementation with the arguments
        """
        if self.num_args is None or len(arguments) == self.num_args:
            return self.implementation(*arguments)
        else:
            raise Exception("Invalid number of arguments. Expected %d, but got %d" % (self.num_args, len(arguments)))

    def eval(self, environment):
        return self

class Call(Expression):
    def __init__(self, operator, *operands):
        super(Expression, self).__init__()
        self.operator = operator
        self.operands = operands

    def eval(self, environment):
        """
        Calls a procedure
        """
        scope = Environment(environment)
        operator = self.operator.eval(scope)
        operands = [operand.eval(scope) for operand in self.operands]
        return operator(*operands)

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

    def __init__(self, value, *args, **kwargs):
        super(Symbol, self).__init__(*args, **kwargs)
        self.value = value

    def __str__(self):
        return "'%s" % self.value

    def eval(self, environment):
        return environment[self].eval(environment)

class Environment(collections.MutableMapping):

    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        # convert keys to symbols
        self.store = dict()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        self.store[self.keytransform(key)] = value

    def __getitem__(self, key):
        key = self.keytransform(key)

        # if the item is in this environment, fine ...
        if key in self.store:
            return self.store[key]
        if self.parent is not None:
            return self.parent[key]
        else:
            return self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __delitem__(self, key):
        del self.store[self.keytransform(key)]

    def keytransform(self, key):
        return Symbol(key)