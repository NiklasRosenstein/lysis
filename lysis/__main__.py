#!/usr/bin/env python2
# Copyright (c) 2013 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import scan
import lysis
import argparse

colored = None
if sys.platform == 'win32':
    try:
        import colorama
    except ImportError:
        colored = lambda x, color: str(x)
    else:
        colorama.init()
if not colored:
    try:
        from termcolor import colored
    except ImportError:
        colored = lambda x, color: str(x)

def fmt_bool_color(x):
    if x:
        return colored('t', 'green')
    else:
        return colored('f', 'red')

def fmt_bool_normal(x):
    if x:
        return 't'
    else:
        return 'f'

def main():
    argp = argparse.ArgumentParser(description='Evaluate propositional '
            'calculus expressions.')
    argp.add_argument('expr', nargs='+', help='One or more expressions to '
            'evaluate.')
    argp.add_argument('-t', '--table', help='Evaluate all possible '
            'combinations of the variables and print out a table. Only valid '
            'for propositional calculus.', action='store_true')
    argp.add_argument('-nw', '--no-warn', help='Disables the warning if '
            'expected output/calculation time exceeds a certain number.',
            action='store_true')
    argp.add_argument('-nc', '--no-color', help='Colorize output.',
            action='store_true')
    args = argp.parse_args()

    # Process arguments.
    fmt_bool = fmt_bool_normal if args.no_color else fmt_bool_color
    colorize = lambda x, color: str(x) if args.no_color else colored

    # Parse the expressions.
    parser = lysis.parser.Parser()
    nodes = []
    variables = set()
    for i, expr in enumerate(args.expr):
        try:
            node, varset = parser.parse(expr)
            variables |= varset
            nodes.append((node, varset))
        except lysis.error.SyntaxError as exc:
            line = "[SyntaxError in expression %d]:" % i
            print line, expr
            print len(line) * " ", exc
            return 1
        except scan.TokenizationError as exc:
            pos = exc.cursor
            line = "[SyntaxError in expression %d]:" % i
            print line, expr
            print len(line) * " ", (pos.column - 1) * colorize('~', 'blue') + colorize('^', 'red')
            return 1

    # Sort the variables into a fixed tuple.
    variables = tuple(sorted(variables))

    # Print a table?
    if args.table and not args.no_warn:
        n = 2 ** len(variables)
        if n > 50:
            answer = raw_input('There are %d possibilities, do you really '
                               'want to print the full table? [y/n]  ' % n)
            if answer.strip().lower() not in ('y', 'yes', 'true'):
                args.table = False
    if args.table:
        # Generate the head-line and under-line.
        headline = ' '
        underline = '-'
        for i, var in enumerate(variables):
            headline += var
            underline += '-'
            if i < len(variables) - 1:
                headline += ' | '
                underline += '-+-'
        for node, varset in nodes:
            strformat = str(node)
            headline += ' | ' + strformat
            underline += '-+-' + len(strformat) * '-'

        print headline
        print underline

        # Evaluate the table.
        for context in lysis.cfactory.TabularContextFactory(variables):
            line = ' '
            for i, var in enumerate(variables):
                line += fmt_bool(context.get(var))
                if i < len(variables) - 1:
                    line += ' | '
            for node, varset in nodes:
                line += ' | ' + fmt_bool(node.evaluate(context)) + (len(str(node)) - 1) * ' '

            print line

if __name__ == "__main__":
    sys.exit(main())

