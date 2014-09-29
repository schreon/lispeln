import collections
from lispeln.scheme.expression import Expression

__author__ = 'schreon'


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