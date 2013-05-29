__author__ = 'Joe Linn'

from .abstractfilter import AbstractFilter
import pylastica.script


class Script(AbstractFilter):
    def __init__(self, script=None):
        """
        @param script: optional
        @type script: str or pylastica.script.Script
        """
        super(Script, self).__init__()
        if script is not None:
            self.set_script(script)

    def set_script(self, script):
        """
        Set the script object
        @param script:
        @type script: str or dict or pylastica.script.Script
        @return:
        @rtype: self
        """
        self.params = pylastica.script.Script.create(script).to_dict()
        return self
