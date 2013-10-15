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
lysis.tree.prop
~~~~~~~~~~~~~~~

"""

from lysis.tree.base import Node


class BaseProposition(Node):

    pass

class Proposition(BaseProposition):

    def __init__(self, name):
        super(Proposition, self).__init__()
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, context):
        return bool(context.get(self.name))


class BaseModifier(BaseProposition):

    def __init__(self, child):
        super(BaseModifier, self).__init__()
        self.child = child

class Negation(BaseModifier):

    def __str__(self):
        return '/%s' % self.child

    def evaluate(self, context):
        return not self.child.evaluate(context)


class BaseOperator(BaseProposition):

    def __init__(self, left, right):
        super(BaseOperator, self).__init__()
        self.left = left
        self.right = right

class And(BaseOperator):

    def __str__(self):
        return '(%s & %s)' % (self.left, self.right)

    def evaluate(self, context):
        return self.left.evaluate(context) and self.right.evaluate(context)

class Or(BaseOperator):

    def __str__(self):
        return '(%s | %s)' % (self.left, self.right)

    def evaluate(self, context):
        return self.left.evaluate(context) or self.right.evaluate(context)

class Implication(BaseOperator):

    def __str__(self):
        return '(%s => %s)' % (self.left, self.right)

    def evaluate(self, context):
        if self.left.evaluate(context):
            return self.right.evaluate(context)
        else:
            return True

class Equality(BaseOperator):

    def __str__(self):
        return '(%s <=> %s)' % (self.left, self.right)

    def evaluate(self, context):
        return bool(self.left.evaluate(context)) == bool(self.right.evaluate(context))



