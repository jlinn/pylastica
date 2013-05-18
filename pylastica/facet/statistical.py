__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.script

class Statistical(AbstractFacet):
    def set_field(self, field):
        """
        Set the field for the stats facet
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)

    def set_fields(self, fields):
        """
        Set multiple fields for the facet
        @param fields: list of field names
        @type fields: list of str
        @return:
        @rtype: self
        """
        return self.set_param('fields', fields)

    def set_script(self, script):
        """
        Set the script to calculate stats
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if not isinstance(script, pylastica.script.Script):
            raise TypeError("script must be of type Script: %r" % script)
        return self.set_param('script', script.script).set_param('params', script.params)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('statistical', self._params)
        return super(Statistical, self).to_dict()


