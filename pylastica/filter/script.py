__author__ = 'Joe Linn'

import pylastica.filter.abstractfilter

class Script(pylastica.filter.abstractfilter.AbstractFilter):
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
