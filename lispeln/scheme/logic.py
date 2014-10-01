from lispeln.scheme.expression import Syntax

class If(Syntax):
    def __init__(self, test, consequent, alternate):
        super(If, self).__init__()
        self.test = test
        self.consequent = consequent
        self.alternate = alternate


class And(Syntax):
    def __init__(self, *args, **kwargs):
        super(And, self).__init__(*args, **kwargs)
        self.args = args
