from lispeln.scheme.expression import Syntax


class Pair(Syntax):
    def __init__(self, first, rest, *args, **kwargs):
        super(Pair, self).__init__(*args, **kwargs)
        self.first = first
        self.rest = rest

    def __eq__(self, other):
        """
        Attention, this is the equality on AST level - not evaluated!
        """
        if not isinstance(other, Pair):
            return False
        else:
            return self.first == other.first and self.rest == other.rest

class Let(Syntax):
    def __init__(self, bindings, expression):
        super(Let, self).__init__()
        self.bindings = bindings
        self.expression = expression

class Begin(Syntax):
    def __init__(self, *expressions):
        super(Begin, self).__init__()
        self.expressions = expressions


class Car(Syntax):  # First
    def __init__(self, pair, *args, **kwargs):
        super(Car, self).__init__(*args, **kwargs)
        self.pair = pair

class Cdr(Syntax):  # Rest
    def __init__(self, pair, *args, **kwargs):
        super(Cdr, self).__init__(*args, **kwargs)
        self.pair = pair