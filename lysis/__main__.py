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
import lysis
from lysis.utils import term
import argparse

def fmt_bool(x):
    if x:
        return term.colorize('t', 'green')
    else:
        return term.colorize('f', 'red')

def main():
    argp = argparse.ArgumentParser(description='Evaluate propositional '
            'calculus and set expressions (latter has yet to be '
            'implemented).')
    argp.add_argument('expr', nargs='+', help='One or more expressions to '
            'evaluate.')
    argp.add_argument('-t', '--table', help='Evaluate all possible '
            'combinations of the variables and print out a table. Only valid '
            'for propositional calculus.', action='store_true')
    argp.add_argument('-nw', '--no-warn', help='Disables the warning if '
            'expected output/calculation time exceeds a certain number.',
            action='store_true')
    args = argp.parse_args()

    # Parse the expressions.
    parser = lysis.parser.Parser()
    nodes = []
    variables = set()
    for expr in args.expr:
        try:
            node, varset = parser.parse(expr)
            variables |= varset
            nodes.append((node, varset))
        except lysis.error.SyntaxError as exc:
            print "[SyntaxError]:", exc
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
        headline = ''
        underline = ''
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
            line = ''
            for i, var in enumerate(variables):
                line += fmt_bool(context.get(var))
                if i < len(variables) - 1:
                    line += ' | '
            for node, varset in nodes:
                line += ' | ' + fmt_bool(node.evaluate(context)) + (len(str(node)) - 1) * ' '

            print line

if __name__ == "__main__":
    sys.exit(main())

