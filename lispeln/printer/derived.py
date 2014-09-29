from lispeln.scheme.constants import Nil, Integer, Float, Boolean
from lispeln.scheme.derived import Cons
from lispeln.scheme.expressions import Symbol

import logging

def ravel(cons):
    """
    :param cons: Cons to convert to python list
    :return: a flat python list representing a (nested) cons
    """
    if not isinstance(cons.rest, Cons):
        return [cons.first, cons.rest]
    else:
        last = cons.rest
        l = [cons.first]
        while isinstance(last, Cons):
            l.append(last.first)
            last = last.rest
        l.append(last)
        return l

def print_symbol(symbol):
    logging.info("print Symbol: %s" % symbol.value)
    return symbol.value

def print_cons(cons):
    logging.info("print cons")
    if isinstance(cons.rest, Cons):
        l = ravel(cons)
        res = "(" + " ".join([print_expression(el) for el in l[:-1]])
        if isinstance(l[-1], Nil):
            res += ")"
        else:
            res += " . "+print_expression(l[-1])+")"

        return res

    if isinstance(cons.rest, Nil):
        return "(%s)" % print_expression(cons.first)

    return "(%s . %s)" % (print_expression(cons.first), print_expression(cons.rest))


def print_number(number):
    logging.info("print number: %s" % str(number.value))
    return str(number.value)

def print_boolean(boolean):
    if boolean.value == True:
        return "#t"
    if boolean.value == False:
        return "#f"
    raise Exception("This is not a boolean. Won't print it.")

def print_nil(nil):
    return "()"

print_dict = {
    Nil: print_nil,
    Boolean: print_boolean,
    Integer: print_number,
    Float: print_number,
    Symbol: print_symbol,
    Cons: print_cons
}
def print_expression(expression):
    print_func = print_dict.get(expression.__class__, None)
    if print_func is None:
        raise Exception("No print function defined for %s" % str(expression.__class__))
    else:
        return print_func(expression)

# def __repr__(self):
#     return "<%s: (%s.%s)>" % (self.__class__.__name__, self.first, self.rest)