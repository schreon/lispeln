__author__ = 'schreon'

class Syntax(object):
    def __repr__(self):
        return "<Syntax:%s>" % self.__class__.__name__

class Define(Syntax):
    """
    symbol, expression
    """

class Set(Syntax):
    """
    symbol, expression
    """

class Let(Syntax):
    """
    [bindings], expression
    """

class Begin(Syntax):
    """
    [expressions]
    """

class Quote(Syntax):
    """
    expression
    """

class If(Syntax):
    """
    test, consequent, alternate
    """


class And(Syntax):
    """
    expressions
    """

class Or(Syntax):
    """
    expressions
    """

class Lambda(Syntax):
    """
    [formals], body
    """
