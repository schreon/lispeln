import collections
import logging
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

class Environment(collections.MutableMapping):

    def __init__(self, parent, *args, **kwargs):
        logging.info("Creating new environment")
        self.parent = parent
        # convert keys to symbols
        self.store = dict()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        key = self.keytransform(key)
        self.store[key] = value

    def __getitem__(self, key):
        key = self.keytransform(key)
        # if the item is in this environment, fine ...
        try:
            return self.store[key]
        except KeyError:
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
        if isinstance(key, Symbol):
            return key.value
        else:
            return key