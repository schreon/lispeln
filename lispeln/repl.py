from lispeln.evaluator.builtins import define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.evaluator.recursive import evaluate
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.scheme import print_expression


def repl():
    env = Environment(None)
    define_builtins(env)
    print ">>> ",
    while True:
        try:
            line = raw_input()
            if line in ['quit', 'exit']:
                break
            tokenlists = tokenize(line)
            for tokens in tokenlists:
                expression = parse(tokens)
                res = evaluate(expression, env)
                if res is not None:
                    print print_expression(res)
                    print ">>> ",
                else:
                    print
        except KeyboardInterrupt:
            print
            break
        except EOFError:
            print
            break #end of file reached
        except Exception as e:
            print e
            print ">>> ",

