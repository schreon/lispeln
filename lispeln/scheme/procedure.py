import logging
from lispeln.scheme.environment import Environment
from lispeln.scheme.expression import Expression

__author__ = 'schreon'


class Procedure(object):

    def __init__(self, implementation, num_args=None, name=None):
        super(Procedure, self).__init__()
        self.name = name
        self.implementation = implementation
        self.num_args = num_args

    def __call__(self, *arguments):
        """
        Calls the implementation with the arguments
        """
        if self.num_args is None or len(arguments) == self.num_args:
            return self.implementation(*arguments)
        else:
            raise Exception("Invalid number of arguments. Expected %d, but got %d" % (self.num_args, len(arguments)))


class Call(Expression):
    def __init__(self, operator, *operands):
        super(Expression, self).__init__()
        self.operator = operator
        self.operands = operands


class Lambda(Expression):
    def __init__(self, formals, body, *args, **kwargs):
        super(Lambda, self).__init__(*args, **kwargs)
        self.formals = formals
        self.body = body

