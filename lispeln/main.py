from lispeln.evaluator.builtins import define_builtins
from lispeln.evaluator.environment import Environment
from lispeln.evaluator.recursive import evaluate
from lispeln.parser.parser import parse
from lispeln.parser.tokenizer import tokenize
from lispeln.printer.scheme import print_expression

import fileinput

def repl():
    env = Environment(None)
    define_builtins(env)
    code = ""
    parentheses = 0
    prompt = ">>> "
    while True:
        try:
            line = raw_input(prompt)
            code += line + "\n"
            parentheses += line.count("(")
            parentheses -= line.count(")")

            if parentheses == 0:
                if code in ['quit', 'exit']:
                    break
                tokenlists = tokenize(code)
                for tokens in tokenlists:
                    expression = parse(tokens)
                    res = evaluate(expression, env)
                    if res is not None:
                        print print_expression(res)
                print
                prompt = ">>> "
                code = ""
            else:
                prompt = ""
        except KeyboardInterrupt:
            print
            break
        except Exception as e:
            print e
            print
            code = ""
            prompt = ">>> "


def batch():
    code = ""
    env = Environment(None)
    define_builtins(env)
    for c in fileinput.input():
        try:
            code += c
        except KeyboardInterrupt:
            print
            break

    try:
        tokenlists = tokenize(code)
        for tokens in tokenlists:
            expression = parse(tokens)
            res = evaluate(expression, env)
            if res is not None:
                print print_expression(res)
    except Exception as e:
        print e

def gui():

    import Tkinter as tk

    root = tk.Tk()
    root.title("Visual Scheme Editor")
    text = tk.Text(root, height=25, width=150)
    output = tk.Text(root, height=25, width=150)

    scope = {}

    def reset():
        scope['env'] = Environment(None)
        define_builtins(scope['env'])


    reset()

    def eval():
        data = text.get("1.0", tk.END)

        output.delete("1.0", tk.END)
        try:
            results = []
            tokenlists = tokenize(data)
            for tokens in tokenlists:
                expression = parse(tokens)
                res = evaluate(expression, scope['env'])
                if res is not None:
                    results.append(print_expression(res))

            output.insert("1.0", "\n".join(results))
        except Exception as e:
            output.insert("1.0", e.message)


    button = tk.Button(root, text='Run', fg="dark green", width=25, command=eval)
    reset_button = tk.Button(root, text='Reset', fg="dark red", width=25, command=reset)

    text.pack()
    button.pack()
    reset_button.pack()
    output.pack()
    root.mainloop()

