from lispeln.scheme.expressions import Expression

class ConstantSingleton(type):
    """
    Metaclass designed for Singletons by argument list. For each argument list there is only one instance.
    """
    _instances = {}
    def __call__(cls, *args):
        key = (cls, args)
        if key not in cls._instances.keys():
            cls._instances[key] = super(ConstantSingleton, cls).__call__(*args)
        return cls._instances[key]

class Constant(Expression):
    __metaclass__ = ConstantSingleton

    def __init__(self, value, *args, **kwargs):
        super(Constant, self).__init__(*args, **kwargs)
        self.value = value

    def eval(self, environment):
        """
        Contants evaluate to themselves
        """
        return self

    def __eq__(self, other):
        return self.value == other.value

class Nil(Constant):
    def __init__(self):
        super(Nil, self).__init__(None)

class Number(Constant):
    def __gt__(self, other):
        return (self.value > other.value)

    def __ge__(self, other):
        return (self.value >= other.value)

    def __lt__(self, other):
        return (self.value < other.value)

    def __le__(self, other):
        return (self.value <= other.value)

    def __ne__(self, other):
        return (self.value != other.value)

    def __eq__(self, other):
        return (self.value == other.value)

class Integer(Number):
    pass

class Float(Number):
    pass

class String(Constant):
    pass

class Boolean(Constant):
    pass