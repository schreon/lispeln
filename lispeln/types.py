import re
import collections

class InvalidValueException(Exception):
    pass

class UndefinedSymbolException(Exception):
    pass


class Type(object):
    impl_type = str
    def __init__(self, value):
        if type(value) != self.impl_type:
            raise InvalidValueException("Expected type %s but got type %s" % (str(type(value)), str(self.impl_type)))
        self.value = value

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if self.value == other:
            return True
        else:
            return False

class Integer(Type):
    impl_type = int

class Float(Type):
    impl_type = float

class String(Type):
    def __str__(self):
        return '"%s"' % self.value

class Boolean(Type):
    impl_type = bool

    def __repr__(self):
        if self.value == True:
            rep = 'true'
        if self.value == False:
            rep = 'false'
        return "<%s:%s>" % (self.__class__.__name__, rep)

    def __str__(self):
        if self.value == True:
            return "#t"
        if self.value == False:
            return "#f"

class SingletonByValue(type):
    """
    Metaclass designed for Symbols. For each Symbol value there is only one Symbol instance.
    """
    _instances = {}
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, cls): # if the value is of the same type, just return the value
            return value

        if value not in cls._instances.keys():
            cls._instances[value] = super(SingletonByValue, cls).__call__(value, *args, **kwargs)
        return cls._instances[value]

class Symbol(Type):
    __metaclass__ = SingletonByValue

    def __str__(self):
        return "'%s" % self.value


class Nil(Type):
    def __init__(self):
        pass

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def __str__(self):
        return "'()"

class Cons(Type):
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def ravel(self):

        """
        Returns this cons as a flat python list.
        :return:
        """
        if not isinstance(self.rest, Cons):
            return [self.first, self.rest]
        else:
            last = self.rest
            l = [self.first]
            while isinstance(last, Cons):
                l.append(last.first)
                last = last.rest
            l.append(last)
            return l

    def __str__(self):
        if isinstance(self.rest, Cons):
            l = self.ravel()
            res = "(" + " ".join([str(el) for el in l[:-1]])
            if isinstance(l[-1], Nil):
                res += ")"
            else:
                res += " . "+str(l[-1])+")"

            return res

        if isinstance(self.rest, Nil):
            return "(%s)" % self.first

        return "(%s . %s)" % (self.first, self.rest)

    def __repr__(self):
        return "<%s: (%s.%s)>" % (self.__class__.__name__, self.first, self.rest)

class Procedure(Type):
    def __init__(self, name, implementation):
        super(Procedure, self).__init__(name)
        self.implementation = implementation

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

    def eval(self, expr):
        if type(expr) in [Integer, Float, String, Boolean]:
            return expr
        elif type(expr) == Symbol:
            try:
                return self.__getitem__(expr)
            except KeyError:
                raise Exception("%s undefined. Cannot reference an identifier before its definition!" % str(expr))
        else:
            expr.eval(self)