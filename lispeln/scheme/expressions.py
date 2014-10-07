import logging

class Expression(object):
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

class SymbolSingleton(type):
    """
    Metaclass designed for Singletons by value. For each value there is only one instance.
    """
    _instances = {}

    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, cls):  # if the value is of the same type, just return the value,
            return value  # so Symbol(Symbol('x')) is the same as Symbol('x')

        if value not in cls._instances:
            cls._instances[value] = super(SymbolSingleton, cls).__call__(value, *args, **kwargs)
        return cls._instances[value]


class Symbol(Expression):
    __metaclass__ = SymbolSingleton

    def __init__(self, value, *args, **kwargs):
        super(Symbol, self).__init__(*args, **kwargs)
        self.value = value

    def __repr__(self):
        return "<Symbol:%s>" % self.value


class Pair(Expression):
    """
    first, rest
    """

    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def __eq__(self, other):
        if not isinstance(other, Pair):
            return False
        if self.first == other.first and self.rest == other.rest:
            return True
        else:
            return False

class Procedure(object):

    def __init__(self, implementation, num_args=None, name=None):
        super(Procedure, self).__init__()
        self.name = name
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

    def __repr__(self):
        return "<procedure:%s>" % str(self.name)
