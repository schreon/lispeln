import sys
from lispeln.evaluator.builtins import define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.evaluator.recursive import evaluate
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.scheme import print_expression


def repl():
    env = Environment(None)
    define_builtins(env)
    while True:
        try:
            line = raw_input(">>> ")
            if line in ['quit', 'exit']:
                sys.exit(0)
            tokenlists = tokenize(line)
            for tokens in tokenlists:
                expression = parse(tokens)
                res = evaluate(expression, env)
                if res is not None:
                    print print_expression(res)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print e