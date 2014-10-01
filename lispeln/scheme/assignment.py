from lispeln.scheme.expression import Syntax

__author__ = 'schreon'


class Define(Syntax):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Define, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression

    def __repr__(self):
        return "<Define:%s -> %s>" % (repr(self.symbol), repr(self.expression))


class Set(Syntax):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Set, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression

    def __repr__(self):
        return "<set:%s -> %s>" % (repr(self.symbol), repr(self.expression))