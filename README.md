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

Usage
==========
Use the command `repl` to start an interactive read-eval-print loop:

    repl
    >>> (+ 1 2)
    3

You can pipe your stdin into lispeln. Please create a file 'test' with the following content:

    (define a 41)
    (+ a 1)

You can now call:
    
    lispeln < test

The result should be:
    
    42

GUI
===
To run `lispeln` in GUI mode, type 

    repl-gui


Run Tests & Coverage
====================
Clone the repo and `cd` into it:

    git clone https://github.com/schreon/lispeln.git lispeln
    cd lispeln

Create another virtualenv, activate it

    virtualenv .env
    source .env/bin/activate

Install py.test and py.test coverage:

    pip install pytest pytest-cov

Add this project to the local `pip`:

    pip install -e .

Run py.test with coverage:

    py.test --cov lispeln tests/

Syntax
======
<table>
    <thead>
        <th>Syntax</th>
        <th>Form</th>
        <th>Example</th>
        <th>Result</th>
    </thead>
    <tr>
        <td>let</td>
        <td><b>let</b> (bindings) expression</td>
        <td>(let ((x 1) (y 2)) (+ x y))</td>
        <td>3</td>
    </tr>
    <tr>
        <td>define</td>
        <td><b>define</b> symbol value</td>
        <td>(define x 42)</td>
        <td></td>
    </tr>
    <tr>
        <td>set!</td>
        <td><b>set!</b> symbol value</td>
        <td>(set! x 13)</td>
        <td></td>
    </tr>
    <tr>
        <td>if</td>
        <td><b>if</b> test consequent alternate</td>
        <td>(if (&lt; 1 2) "a" "b")</td>
        <td>"a"</td>
    </tr>
    <tr>
        <td>and</td>
        <td><b>and</b> tests</td>
        <td>(and #t "hello" #t)</td>
        <td>#t</td>
    </tr>
    <tr>
        <td>or</td>
        <td><b>or</b> tests</td>
        <td>(or #f "hello" #t)</td>
        <td>"hello"</td>
    </tr>
    <tr>
        <td>lambda</td>
        <td><b>lambda</b> formals body</td>
        <td>((lambda (n) (set! n (+ n 1)) (set! n (* n 2)) n) 4)</td>
        <td>10</td>
    </tr>
    <tr>
        <td>begin</td>
        <td><b>begin</b> expressions</td>
        <td>(begin (define x 13) (set! x 41) (+ x 1))</td>
        <td>42</td>
    </tr>
    <tr>
        <td>'</td>
        <td><b>'</b> expression</td>
        <td>'(something)</td>
        <td>(something)</td>
    </tr>
</table>


Built-Ins
=========
The following built-in procedures are implemented:

<table>
    <thead>
        <th>Symbol</th>
        <th>Procedure</th>
        <th>Example</th>
        <th>Result</th>
    </thead>
    <tr>
        <td>+</td>
        <td>plus</td>
        <td>(+ 1 2 3)</td>
        <td>6</td>
    </tr>
    <tr>
        <td>-</td>
        <td>minus</td>
        <td>(- 1 2 3)</td>
        <td>-4</td>
    </tr>
    <tr>
        <td>*</td>
        <td>multiply</td>
        <td>(* 4 5 6)</td>
        <td>120</td>
    </tr>
    <tr>
        <td>/</td>
        <td>divide</td>
        <td>(/ 8 2 2)</td>
        <td>2</td>
    </tr>
    <tr>
        <td>=</td>
        <td>numerical equality</td>
        <td>(= 1 2)</td>
        <td>#f</td>
    </tr>
    <tr>
        <td>eq?</td>
        <td>equality</td>
        <td>(eq? "b" "b")</td>
        <td>#t</td>
    </tr>
    <tr>
        <td>&lt;</td>
        <td>less than</td>
        <td>(&lt; 2 1)</td>
        <td>#f</td>
    </tr>
    <tr>
        <td>&gt;</td>
        <td>greater than</td>
        <td>(&gt; 2 1)</td>
        <td>#t</td>
    </tr>
    <tr>
        <td>&lt;=</td>
        <td>less or equal</td>
        <td>(&lt;= 2 2)</td>
        <td>#t</td>
    </tr>
    <tr>
        <td>&gt;=</td>
        <td>greater or equal</td>
        <td>(&gt;= 2 2)</td>
        <td>#t</td>
    </tr>
    <tr>
        <td>cons</td>
        <td>create pair</td>
        <td>(cons 1 2)</td>
        <td>(1 . 2)</td>
    </tr>
    <tr>
        <td>car</td>
        <td>return first of pair</td>
        <td>(car (cons &quot;a&quot; &quot;b&quot;))</td>
        <td>&quot;a&quot;</td>
    </tr>
    <tr>
        <td>cdr</td>
        <td>return rest of pair</td>
        <td>(cdr (cons &quot;a&quot; &quot;b&quot;))</td>
        <td>&quot;b&quot;</td>
    </tr>
</table>
