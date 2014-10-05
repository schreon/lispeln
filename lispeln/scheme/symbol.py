from lispeln.scheme.expression import Expression


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
