from lispeln.evaluator.builtins import define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.evaluator.recursive import evaluate
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.scheme import print_expression

import sys

def repl():
    if '-i' in sys.argv or '--interactive' in sys.argv:
        prompt = ">>> "
    else:
        prompt = ""
    env = Environment(None)
    define_builtins(env)
    while True:
        try:
            line = raw_input(prompt)
            if line in ['quit', 'exit']:
                break
            tokenlists = tokenize(line)
            for tokens in tokenlists:
                expression = parse(tokens)
                res = evaluate(expression, env)
                if res is not None:
                    print print_expression(res)
        except KeyboardInterrupt:
            print
            break
        except EOFError:
            break #end of file reached
        except Exception as e:
            print e