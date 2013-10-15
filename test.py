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
import argparse

def main():
    argp = argparse.ArgumentParser(description='Evaluate propositional '
            'calculus and set expressions (latter has yet to be '
            'implemented).')
    argp.add_argument('expr', help='The expression to evaluate.')
    argp.add_argument('-t', '--table', help='Evaluate all possible '
            'combinations of the variables and print out a table. Only valid '
            'for propositional calculus.', action='store_true')
    argp.add_argument('-nw', '--no-warn', help='Disables the warning if '
            'expected output/calculation time exceeds a certain number.',
            action='store_true')
    argp.add_argument('-d', '--debug', help='Print debug information (eg. '
            'the variables that have been found and a re-stringified '
            'representation of the expression.', action='store_true')
    args = argp.parse_args()

    # Parse the expression.
    parser = lysis.parser.Parser()
    try:
        node, varset = parser.parse(args.expr)
    except lysis.error.SyntaxError as exc:
        print "[SyntaxError]:", exc
        return 1

    # Print debug stuff?
    if args.debug:
        print
        print "Expression: ", node
        print "Variables:  ", varset
        print

    # Print a table?
    if args.table and not args.no_warn:
        n = 2 ** len(varset)
        if n > 50:
            answer = raw_input('There are %d possibilities, do you really '
                               'want to print the full table? [y/n]  ' % n)
            if answer.strip().lower() not in ('y', 'yes', 'true'):
                args.table = False
    if args.table:
        pass


if __name__ == "__main__":
    sys.exit(main())

