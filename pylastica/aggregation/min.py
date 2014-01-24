from pylastica.aggregation.abstractaggregation import AbstractAggregation
from pylastica.script import Script

__author__ = 'Joe Linn'


class Min(AbstractAggregation):
    def set_field(self, field):
        """
        Set the field for this aggregation
        @param field: the name of the document field on which to perform this aggregation
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param("field", field)

    def set_script(self, script):
        """
        Set a script for this aggregation
        @param script: if a Script object is passed, its params will be used
        @type script: str or Script
        @return:
        @rtype: self
        """
        if isinstance(script, Script):
            self.set_param("params", script.params)
            script = script.script
        return self.set_param("script", script)