from lispeln.scheme.expression import Expression


class Cons(Expression):
    def __init__(self, first, rest, *args, **kwargs):
        super(Cons, self).__init__(*args, **kwargs)
        self.first = first
        self.rest = rest

class Let(Expression):
    def __init__(self, definitions, expression):
        super(Let, self).__init__()
        self.definitions = definitions
        self.expression = expression

class Begin(Expression):
    def __init__(self, *expressions):
        super(Begin, self).__init__()
        self.expressions = expressions

class Cdr(Expression):
    def __init__(self, cons, *args, **kwargs):
        super(Cdr, self).__init__(*args, **kwargs)
        self.cons = cons

class IsEmpty(Expression):
    def __init__(self, cons, *args, **kwargs):
        super(IsEmpty, self).__init__(*args, **kwargs)
        self.cons = cons
