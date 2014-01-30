
__author__ = 'Joe Linn'

import abc
import pylastica.param
import pylastica.script


class AbstractAggregation(pylastica.param.Param):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        super(AbstractAggregation, self).__init__()
        self._name = None
        self.name = name
        self._aggs = {}

    @property
    def name(self):
        """
        Get the name of this facet
        @return:
        @rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of this facet.
        @param name:
        @type name: str
        """
        if not isinstance(name, str) or name == '':
            raise TypeError("name must be a string: %r" % name)
        self._name = name

    def add_aggregation(self, aggregation):
        """
        Add a sub-aggregation
        @param aggregation: a sub-aggregation
        @type aggregation: AbstractAggregation
        @return:
        @rtype: self
        """
        if not isinstance(aggregation, AbstractAggregation):
            raise TypeError("aggregation must be an implementation of AbstractAggregation: %r" % aggregation)
        self._aggs[aggregation.name] = aggregation.to_dict()
        return self

    @property
    def aggs(self):
        return self._aggs

    def to_dict(self):
        """
        @return:
        @rtype: dict
        """
        dictionary = super(AbstractAggregation, self).to_dict()
        if len(self._aggs):
            dictionary['aggs'] = self._aggs
        return dictionary


class SimpleAggregation(AbstractAggregation):
    __metaclass__ = abc.ABCMeta

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
        if isinstance(script, pylastica.script.Script):
            self.set_param("params", script.params)
            script = script.script
        return self.set_param("script", script)