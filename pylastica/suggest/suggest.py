__author__ = 'Joe Linn'

from pylastica.param import Param


class Suggest(Param):
    """
    @see: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-suggesters.html
    """
    def __init__(self, suggestion=None):
        """
        @param suggestion: optional
        @type suggestion:  pylastica.suggest.abstract.AbstractSuggestion
        """
        super(Suggest, self).__init__()
        if suggestion is not None:
            self.add_suggestion(suggestion)

    def set_global_text(self, text):
        """
        Set the global text for this suggester
        @param text:
        @type text: str
        @rtype: self
        """
        return self.set_param("text", text)

    def add_suggestion(self, suggestion):
        """
        Add a suggestion to this suggest clause
        @param suggestion:
        @type suggestion: pylastica.suggest.abstract.AbstractSuggestion
        @return:
        @rtype: self
        """
        self.set_param(suggestion.name, suggestion.to_dict())
