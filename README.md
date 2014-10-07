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
Use the command `repl -i` or `repl --interactive` to start an interactive read-eval-print loop:

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
