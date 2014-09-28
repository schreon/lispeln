from lispeln.expressions import Expression


class Constant(Expression):
    def __init__(self, value):
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

class Integer(Constant):
    pass

class Float(Constant):
    pass

class String(Constant):
    def __str__(self):
        return '"%s"' % self.value

class Boolean(Constant):
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