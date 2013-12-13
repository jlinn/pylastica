__author__ = 'Joe Linn'

import abc
from pylastica.param import Param


class AbstractSuggestion(Param):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, field):
        """
        @param name: the name of this suggestion
        @type name: str
        @param field: the field on which to perform this suggestion
        @type field: str
        """
        super(AbstractSuggestion, self).__init__()
        self._name = ''
        self._text = None
        self._name = name
        self.set_field(field)

    def set_text(self, text):
        """
        Suggest text must be set either globally or per suggestion
        @param text: text to use for this suggestion
        @type text: str
        @rtype: self
        """
        self._text = text
        return self

    def set_field(self, field):
        """
        Set the field on which to perform this suggestion operation
        @param field: field name
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param('field', field)

    def set_size(self, size):
        """
        Set the maximum number of suggestions to return
        @param size: a positive integer
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param("size", int(size))

    def set_shard_size(self, size):
        """
        Set the maximum number of suggestions to be retrieved from each shard
        @param size: a positive integer
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param("shard_size", int(size))

    @property
    def name(self):
        """
        @return: the name set for this suggestion
        @rtype: str
        """
        return self._name

    def to_dict(self):
        """

        @return:
        @rtype: dict
        """
        dictionary = super(AbstractSuggestion, self).to_dict()
        if self._text is not None:
            dictionary['text'] = self._text
        return dictionary
