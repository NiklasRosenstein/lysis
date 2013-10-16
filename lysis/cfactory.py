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
lysis.cfactory
~~~~~~~~~~~~~

"""

from lysis.tree import Context

class ContextFactory(object):

    def __iter__(self):
        raise NotImplementedError

class TabularContextFactory(ContextFactory):

    def __init__(self, varset):
        super(TabularContextFactory, self).__init__()
        self.varset = tuple(varset)

    def __iter__(self):
        context = Context()
        for item in self._generate(0, context):
            yield item

    def _generate(self, var_index, context):
        if var_index < len(self.varset):
            context.set(self.varset[var_index], True)
            for item in self._generate(var_index + 1, context):
                yield item
            context.set(self.varset[var_index], False)
            for item in self._generate(var_index + 1, context):
                yield item
        elif var_index >= len(self.varset):
            yield context.copy()
        else:
            assert False, "got var_index < 0"

