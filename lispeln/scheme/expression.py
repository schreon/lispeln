class Expression(object):
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        raise Exception("No representation implemented for %s" % str(self.__class__))

    def __str__(self):
        raise Exception("No string representation implemented for %s" % str(self.__class__))

    def __eq__(self, other):
        raise Exception('equality is not defined on expression %s' % str(self.__class__))

    def __ne__(self, other):
        raise Exception('unequality is not defined on expression %s' % str(self.__class__))

    def __lt__(self, other):
        raise Exception('less-than-operator is not defined on expression %s' % str(self.__class__))

    def __le__(self, other):
        raise Exception('less-equals-operator is not defined on expression %s' % str(self.__class__))

    def __gt__(self, other):
        raise Exception('greater-than-operator is not defined on expression %s' % str(self.__class__))

    def __ge__(self, other):
        raise Exception('greater-equals-operator is not defined on expression %s' % str(self.__class__))

class Quote(Expression):
    def __init__(self, expression, *args, **kwargs):
        super(Quote, self).__init__(*args, **kwargs)
        self.expression = expression
