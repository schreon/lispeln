import collections

class Expression(object):
    def __init__(self, *args, **kwargs):
        pass

    def eval(self, *args, **kwargs):
        pass

    def __repr__(self):
        raise Exception("No representation implemented for %s" % str(self.__class__))

    def __str__(self):
        raise Exception("No string representation implemented for %s" % str(self.__class__))

    def __eq__(self, other):
        raise Exception('equality is not defined on expression %s' % str(self.__class__))

    def __ne__(self, other):
        raise Exception('unequality is not defined on expression %s' % str(self.__class__))

    def __lt__(self, other):
        raise Exception('less-than-operator is not defined on expression %s' % str(self.__class__))

    def __le__(self, other):
        raise Exception('less-equals-operator is not defined on expression %s' % str(self.__class__))

    def __gt__(self, other):
        raise Exception('greater-than-operator is not defined on expression %s' % str(self.__class__))

    def __ge__(self, other):
        raise Exception('greater-equals-operator is not defined on expression %s' % str(self.__class__))


class Conditional(Expression):
    def __init__(self, test, consequent, alternate):
        super(Conditional, self).__init__()
        self.test = test
        self.consequent = consequent
        self.alternate = alternate

    def eval(self, env):
        if self.test.eval(env).value == True:
            return self.consequent.eval(env)
        else:
            return self.alternate.eval(env)

class Define(Expression):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Define, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression

    def eval(self, env):
        env[self.symbol] = self.expression.eval(env)

class Set(Expression):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Set, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression

    def eval(self, env):
        if self.symbol not in env:
            raise Exception("Unknown Symbol %s" % str(self.symbol))
        env[self.symbol] = self.expression.eval(env)

class Quote(Expression):
    def __init__(self, expression, *args, **kwargs):
        super(Quote, self).__init__(*args, **kwargs)
        self.expression = expression

    def eval(self, env):
        return self.expression

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
        operator = self.operator.eval(environment)
        operands = [operand.eval(environment) for operand in self.operands]
        return operator(*operands)


class Lambda(Expression):
    def __init__(self, formals, body, *args, **kwargs):
        super(Lambda, self).__init__(*args, **kwargs)
        self.formals = formals
        self.body = body

    def eval(self, environment):
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

        return Procedure(implementation, num_args=len(self.formals))

class SymbolSingleton(type):
    """
    Metaclass designed for Singletons by value. For each value there is only one instance.
    """
    _instances = {}
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, cls):  # if the value is of the same type, just return the value
            return value

        if value not in cls._instances.keys():
            cls._instances[value] = super(SymbolSingleton, cls).__call__(value, *args, **kwargs)
        return cls._instances[value]

class Symbol(Expression):
    __metaclass__ = SymbolSingleton

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