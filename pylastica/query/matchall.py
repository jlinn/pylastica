__author__ = 'Joe Linn'

import pylastica

class MatchAll(pylastica.query.AbstractQuery):
    def __init__(self):
        self._params = {}
