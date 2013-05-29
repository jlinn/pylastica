__author__ = 'Joe Linn'

import pylastica.param
import pylastica.exception
import pylastica.script

class ScriptFields(pylastica.param.Param):
    def __init__(self, scripts=None):
        """
        @param scripts: dict of name: Script
        @type scripts: dict of (str, pylastica.script.Script)
        """
        super(ScriptFields, self).__init__()
        if scripts is not None:
            self.set_scripts(scripts)

    def add_script(self, name, script):
        """
        Add a script
        @param name: name of the script field
        @type name: str
        @param script: the script
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        assert isinstance(name, str), "name must be a string: %r" % name
        assert len(name) > 0, "name must be set"
        return self.set_param(name, script.to_dict())

    def set_scripts(self, scripts):
        """
        Set multiple scripts
        @param scripts: dict of name: Script
        @type scripts: dict of (str, pylastica.script.Script)
        @return:
        @rtype: self
        """
        self._params = {}
        for name, script in scripts.iteritems():
            self.add_script(name, script)
        return self

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        return self._params
