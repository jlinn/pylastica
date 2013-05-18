__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.exception


class Range(AbstractFacet):
    def set_field(self, field):
        """
        Set the field for the facet
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)

    def set_key_value_fields(self, key_field, value_field):
        """
        Set the fields by their separate key and value fields
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
        SEt the key and value scripts for the facet
        @param key_script:
        @type key_script: str
        @param value_script:
        @type value_script: str
        @return:
        @rtype: self
        """
        return self.set_param('key_script', key_script).set_param('value_script', value_script)

    def set_ranges(self, ranges):
        """
        Set all ranges for this facet
        @param ranges:
        @type ranges: list of dict
        @return:
        @rtype: self
        """
        return self.set_param('ranges', ranges)

    def add_range(self, range_from=None, range_to=None):
        """
        Add a range to the facet
        @param range_from: optional. If omitted, is assumed to be boundless.
        @type range_from: int or float
        @param range_to: optional. Assumed to be boundless if omitted.
        @type range_to: int or float
        @return:
        @rtype: self
        """
        if range_from is None and range_to is None:
            raise pylastica.exception.InvalidException("At least one of range_from and range_to must be set.")
        range_dict = {}
        if range_from is not None:
            range_dict['from'] = range_from
        if range_to is not None:
            range_dict['to'] = range_to
        return self.add_param('ranges', range_dict)

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        field_types_set = 0
        if 'field' in self._params:
            field_types_set += 1
        if 'key_field' in self._params:
            field_types_set += 1
        if 'key_script' in self._params:
            field_types_set += 1
        if field_types_set == 0:
            raise pylastica.exception.InvalidException("One of field, key_field or key_script must be set.")
        elif field_types_set > 1:
            raise pylastica.exception.InvalidException("Either field, key_field, or key_script should be set, but not multiple.")
        self._set_facet_param('range', self._params)
        return super(Range, self).to_dict()



