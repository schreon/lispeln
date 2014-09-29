from lispeln.expressions import Expression

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

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def __str__(self):
        return "'()"

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
    def __str__(self):
        return '"%s"' % self.value

class Boolean(Constant):
    def __repr__(self):
        rep = None
        if self.value == True:
            rep = 'true'
        if self.value == False:
            rep = 'false'
        if rep is None:
            raise Exception("Invalid value: %s" % str(self.value))
        return "<%s:%s>" % (self.__class__.__name__, rep)

    def __str__(self):
        if self.value == True:
            return "#t"
        if self.value == False:
            return "#f"