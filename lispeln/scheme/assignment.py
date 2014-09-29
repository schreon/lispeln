from lispeln.scheme.expression import Expression

__author__ = 'schreon'


class Define(Expression):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Define, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression



class Set(Expression):
    def __init__(self, symbol, expression, *args, **kwargs):
        super(Set, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expression = expression
