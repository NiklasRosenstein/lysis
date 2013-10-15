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
lysis.tree.base
~~~~~~~~~~~~~~~

"""

import warnings

from lysis.error import ExpressionError, ContextResolveError

class Node(object):

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError

    def __contains__(self, other):
        raise ExpressionError("%s is not a set." % self)

    def evaluate(self, context):
        raise NotImplementedError

class Context(object):

    def __init__(self):
        super(Context, self).__init__()
        self.vars = {}

    def set(self, name, value):
        if not isinstance(value, bool):
            warnings.warn("passing non-bool value to Context.set", UserWarning)
        self.vars[name] = value

    def get(self, name):
        if name not in self.vars:
            raise ContextResolveError('context could not resolve "%s"' % name)
        return bool(self.vars[name])



