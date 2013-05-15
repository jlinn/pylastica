__author__ = 'Joe Linn'

from . import abstract

class MatchAll(abstract.AbstractQuery):
    def __init__(self):
        super(MatchAll, self).__init__()
        self._params = {}
