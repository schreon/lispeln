Lispeln
=======

This is a Scheme interpreter written in Python.

Installation
============

If not already done, please install virtualenv into your root python installation:

    pip install virtualenv

Now create a new virtualenv:

    virtualenv .env
    
Activate it:

    source .env/bin/activate


Now install `lispeln` directly from github:

    pip install git+https://github.com/schreon/lispeln.git

Test the repl:

    repl
    >>> (+ 1 2)
    3

Quickstart
==========
Just use the command `repl -i` or `repl --interactive` to start an interactive read-eval-print loop:

    repl -i
    >>> (+ 1 2)
    3

You can pipe your stdin into this repl. Please create a file 'test' with the following content:

    (define a 41)
    (+ a 1)

You can now call:
    
    repl < test

The result should be:
    
    42
