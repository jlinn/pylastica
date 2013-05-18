__author__ = 'Joe Linn'

from .abstractfacet import AbstractFacet
import pylastica.script

class Terms(AbstractFacet):
    ORDER_COUNT = 'count'
    ORDER_TERM = 'term'
    ORDER_REVERSE_COUNT = 'reverse_count'
    ORDER_REVERSE_TERM = 'reverse_term'

    def set_field(self, field):
        """
        Set the field for this facet
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)

    def set_script(self, script):
        """
        Set the script for this facet
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if not isinstance(script, pylastica.script.Script):
            raise TypeError("script must be of type Script: %r" % script)
        return self.set_param('script', script.script).set_param('params', script.params)

    def set_script_field(self, script):
        """
        Set the script field, to be used if no field is provided
        @param script:
        @type script: pylastica.script.Script
        @return:
        @rtype: self
        """
        if not isinstance(script, pylastica.script.Script):
            raise TypeError("script must be of type Script: %r" % script)
        return self.set_param('script_field', script.script).set_param('params', script.params)

    def set_fields(self, fields):
        """
        Set multiple fields for terms
        @param fields:
        @type fields: list of str
        @return:
        @rtype: self
        """
        return self.set_param('fields', fields)

    def set_all_terms(self, all_terms=True):
        """
        Sets the flag to return all available terms. If the term does not have a hit, the count is 0.
        @param all_terms:
        @type all_terms: bool
        @return:
        @rtype: self
        """
        return self.set_param('all_terms', bool(all_terms))

    def set_order(self, order):
        """
        Set the ordering for this facet
        @param order: See ORDER_* class properties for options
        @type order: str
        @return:
        @rtype: self
        """
        return self.set_param('order', order)

    def set_exclude(self, exclude):
        """
        Sets a list of terms which are excluded from the search
        @param exclude:
        @type exclude: list of str
        @return:
        @rtype: self
        """
        return self.set_param('exclude', exclude)


    def set_size(self, size):
        """
        Set the number of terms to return
        @param size:
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param('size', int(size))

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        self._set_facet_param('terms', self._params)
        return super(Terms, self).to_dict()

