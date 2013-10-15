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
    set_.add('prop', 0, scan.CharacterSet(string.uppercase, max_length=1))
    set_.add('ws', 0, scan.CharacterSet(string.whitespace))
    set_.ws.skip = True

    return set_

class Parser(object):

    def __init__(self, tokenset=None):
        super(Parser, self).__init__()
        self.tokenset = tokenset or get_tokenset()

    def parse(self, expr):
        lexer = scan.Lexer.from_string(expr, self.tokenset)
        varset = set()
        token = lexer.read_token()
        enclosed = token.type == lexer.t_g_start
        if enclosed:
            lexer.read_token()
        return self._group(lexer, varset, enclosed), varset

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

            node = self._operator(lexer, varset, node)

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
            return left

        lexer.read_token()
        right = self._expression(lexer, varset)
        return op_type(left, right)








