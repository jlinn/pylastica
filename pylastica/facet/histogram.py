__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet

class Histogram(AbstractFacet):
    def set_field(self, field):
        """
        Set the field for the histogram
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)

    def set_interval(self, interval):
        """
        Set the interval value
        @param interval:
        @type interval: str
        @return:
        @rtype: self
        """
        return self.set_param('interval', interval)

    def set_key_value_fields(self, key_field, value_field):
        """
        Set key_field and value_field
        @param key_field:
        @type key_field: str
        @param value_field:
        @type value_field: str
        @return:
        @rtype: self
        """
        return self.set_param('key_field', key_field).set_param('value_field', value_field)

    def set_key_value_scripts(self, key_script, value_script):
        """
        Set key and value scripts
        @param key_script:
        @type key_script: str
        @param value_script:
        @type value_script: str
        @return:
        @rtype: self
        """
        return self.set_param('key_script', key_script).set_param('value_script', value_script)

    def set_script_params(self, params):
        """
        Set params to be used with scripts
        @param params:
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param('params', params)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('histogram', self._params)
        return super(Histogram, self).to_dict()


