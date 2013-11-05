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
r"""
lysis.parser
~~~~~~~~~~~~

"""

import scan
import string

from lysis.error import SyntaxError
from lysis.tree import prop

def get_tokenset():
    set_ = scan.TokenSet()
    set_.add('g_start', 0, scan.Keyword('('))
    set_.add('g_end', 0, scan.Keyword(')'))
    set_.add('neg', 0, scan.Keyword('/'))
    set_.add('and', 0, scan.Keyword('&'))
    set_.add('or', 0, scan.Keyword('|'))
    set_.add('impl', 0, scan.Keyword('=>'))
    set_.add('equal', 0, scan.Keyword('<=>'))
    set_.add('prop', 0, scan.CharacterSet(string.uppercase))
    set_.add('ws', 0, scan.CharacterSet(string.whitespace))
    set_.ws.skip = True

    # Set up operator priorities.
    and_ = getattr(set_, 'and')
    and_.priority = 100

    or_ = getattr(set_, 'or')
    or_.priority = 200

    set_.impl.priority = 50
    set_.equal.priority = 50

    return set_

class Parser(object):

    def __init__(self, tokenset=None):
        super(Parser, self).__init__()
        self.tokenset = tokenset or get_tokenset()

    def parse(self, expr):
        lexer = scan.Lexer.from_string(expr, self.tokenset)
        lexer.read_token()
        return self.parse_from_lexer(lexer)

    def parse_from_lexer(self, lexer):
        varset = set()
        return self._group(lexer, varset, False), varset

    def _group(self, lexer, varset, enclosed=True):
        if lexer.token.type == lexer.t_g_end:
            if enclosed:
                raise SyntaxError('empty paranthesis', lexer.token)
            else:
                raise SyntaxError('unexpected closing paranthesis', lexer.token)

        node = self._expression(lexer, varset)
        while lexer.token:
            if enclosed and lexer.token.type == lexer.t_g_end:
                break

            new_node = self._operator(lexer, varset, node)
            if new_node is node:
                break
            node = new_node

        if enclosed and lexer.token.type != lexer.t_g_end:
            raise SyntaxError('expected closing paranthesis', lexer.token)
        elif enclosed:
            lexer.read_token()

        return node

    def _expression(self, lexer, varset):
        if lexer.token.type == lexer.t_prop:
            varset.add(lexer.token.value)
            node = prop.Proposition(lexer.token.value)
            lexer.read_token()
        elif lexer.token.type == lexer.t_neg:
            lexer.read_token()
            node = prop.Negation(self._expression(lexer, varset))
        elif lexer.token.type == lexer.t_g_start:
            lexer.read_token()
            node = self._group(lexer, varset, True)
        else:
            raise SyntaxError('expected expression', lexer.token)

        return node

    def _operator(self, lexer, varset, left):
        nodes = [left]
        operators = []

        while True:
            if lexer.token.type == lexer.t_and:
                op_type = prop.And
            elif lexer.token.type == lexer.t_or:
                op_type = prop.Or
            elif lexer.token.type == lexer.t_impl:
                op_type = prop.Implication
            elif lexer.token.type == lexer.t_equal:
                op_type = prop.Equality
            elif not lexer.token.invalid and lexer.token.type != lexer.t_g_end:
                raise SyntaxError('expected nothing or expression', lexer.token)
            else:
                break

            priority = lexer.token.type.priority
            while operators and operators[-1][1] > priority:
                op, prior = operators.pop()
                assert len(nodes) > 1
                r, l = nodes.pop(), nodes.pop()
                nodes.append(op(l, r))

            operators.append([op_type, lexer.token.type.priority])
            lexer.read_token()
            nodes.append(self._expression(lexer, varset))

        for op, prior in reversed(operators):
            assert len(nodes) > 1
            r, l = nodes.pop(), nodes.pop()
            nodes.append(op(l, r))

        assert len(nodes) == 1
        return nodes[0]








