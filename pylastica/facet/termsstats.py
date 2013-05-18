__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.script


class TermsStats(AbstractFacet):
    def set_key_field(self, key_field):
        """
        Sets the key field for the query
        @param key_field:
        @type key_field: str
        @return:
        @rtype: self
        """
        return self.set_param('key_field', key_field)

    def set_value_script(self, script):
        """
        Set a script to calculate the statistical information on a per term basis
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if isinstance(script, pylastica.script.Script):
            raise TypeError("script must be of type Script: %r" % script)
        return self.set_param('value_script', script.script).set_param('params', script.params)

    def set_value_field(self, field):
        """
        Set the field on which to compute stats
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('value_field', field)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('terms_stats', self._params)
        return super(TermsStats, self).to_dict()


