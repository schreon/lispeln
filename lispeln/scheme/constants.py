from lispeln.scheme.expression import Expression

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
        if type(value) != self.internal_type:
            raise Exception("Invalid type %s, excpected %s" % (str(type(value)), str(self.internal_type)))
        super(Constant, self).__init__(*args, **kwargs)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, str(self.value))

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
    internal_type = int

class Float(Number):
    internal_type = float

class String(Constant):
    internal_type = str

class Boolean(Constant):
    internal_type = bool