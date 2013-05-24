__author__ = 'Joe Linn'

from .abstract import AbstractQuery


class MoreLikeThis(AbstractQuery):
    def set_fields(self, fields):
        """
        Set fields for this query
        @param fields:
        @type fields: list of str
        @return:
        @rtype: self
        """
        return self.set_param('fields', fields)

    def set_like_text(self, text):
        """
        Set the like_text value
        @param text:
        @type text: str
        @return:
        @rtype: self
        """
        return self.set_param('like_text', text.strip())

    def set_boost(self, boost):
        """
        Set the boost
        @param boost:
        @type boost: float
        @return:
        @rtype: self
        """
        return self.set_param('boost', float(boost))

    def set_max_query_terms(self, max_query_terms):
        """
        Set max_query_terms
        @param max_query_terms:
        @type max_query_terms: int
        @return:
        @rtype: self
        """
        return self.set_param('max_query_terms', int(max_query_terms))

    def set_percent_terms_to_match(self, percent):
        """
        Set percent terms to match
        @param percent:
        @type percent: float
        @return:
        @rtype: self
        """
        return self.set_param('percent_terms_to_match', float(percent))

    def set_min_term_frequency(self, min_frequency):
        """
        Set minimum term frequency
        @param min_frequency:
        @type min_frequency: int
        @return:
        @rtype: self
        """
        return self.set_param('min_term_freq', int(min_frequency))

    def set_min_doc_frequency(self, min_freq):
        """
        Set minimum document frequency
        @param min_freq:
        @type min_freq: int
        @return:
        @rtype: self
        """
        return self.set_param('min_doc_freq', int(min_freq))

    def set_max_doc_frequency(self, max_freq):
        """
        Set the maximum doc frequency
        @param max_freq:
        @type max_freq: int
        @return:
        @rtype: self
        """
        return self.set_param('max_doc_freq', int(max_freq))

    def set_min_word_length(self, length):
        """
        Set minimum word length
        @param length:
        @type length: int
        @return:
        @rtype: self
        """
        return self.set_param('min_word_length', int(length))

    def set_max_word_length(self, length):
        """
        Set maximum word length
        @param length:
        @type length: int
        @return:
        @rtype: str
        """
        return self.set_param('max_word_length', length)

    def set_boost_terms(self, terms):
        """
        Set boost terms
        @param terms:
        @type terms: bool
        @return:
        @rtype: self
        """
        return self.set_param('boost_terms', bool(terms))

    def set_analyzer(self, analyzer):
        """
        Set analyzer
        @param analyzer:
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_param('analyzer', analyzer.strip())

    def set_stop_words(self, stop_words):
        """
        Set stop words
        @param stop_words:
        @type stop_words: list of str
        @return:
        @rtype: self
        """
        assert isinstance(stop_words, list), "stop_words must be a list: %r" % stop_words
        return self.set_param('stop_words', stop_words)
