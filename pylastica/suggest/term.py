__author__ = 'Joe Linn'

from .abstract import AbstractSuggestion


class Term(AbstractSuggestion):
    """
    @see: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-suggesters-term.html
    """

    SORT_SCORE = 'score'
    SORT_FREQUENCY = 'frequency'

    SUGGEST_MODE_MISSING = 'missing'
    SUGGEST_MODE_POPULAR = 'popular'
    SUGGEST_MODE_ALWAYS = 'always'

    def set_analyzer(self, analyzer):
        """
        Set the analyzer to be used for this suggest operation
        @param analyzer: the name of a pre-defined analyzer
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_param("analyzer", analyzer)

    def set_sort(self, sort):
        """
        Set the sorting method for results
        @param sort: see SORT_* constants for options
        @type sort: str
        @return:
        @rtype: self
        """
        return self.set_param("sort", sort)

    def set_suggest_mode(self, mode):
        """

        @param mode: see SUGGEST_MODE_* constants for options
        @type mode: str
        @return:
        @rtype: self
        """
        return self.set_param("suggest_mode", mode)

    def set_lowercase_terms(self, lowercase=True):
        """
        If true, suggest terms will be lower cased after text analysis
        @param lowercase:
        @type lowercase: bool
        @return:
        @rtype: self
        """
        return self.set_param("lowercase_terms", bool(lowercase))

    def set_max_edits(self, max_edits):
        """
        Set the maximum edit distance candidate suggestions can have in order to be considered as a suggestion
        @param max_edits: A value between 1 and 2. Defaults to 2.
        @type max_edits: float
        @return:
        @rtype: self
        """
        return self.set_param("max_edits", max_edits)

    def set_prefix_length(self, length):
        """
        The number of minimum prefix characters that must match in order to be a suggestion candidate
        @param length: Defaults to 1
        @type length: int
        @return:
        @rtype: self
        """
        return self.set_param("prefix_len", length)

    def set_min_word_length(self, length):
        """
        The minimum length a suggest text term must have in order to be included.
        @param length: Defaults to 4
        @type length: int
        @return:
        @rtype: self
        """
        return self.set_param("min_word_len", length)

    def set_max_inspections(self, max_inspections):
        """

        @param max_inspections: Defaults to 5
        @type max_inspections: int
        @return:
        @rtype: self
        """
        return self.set_param("max_inspections", max_inspections)

    def set_min_doc_frequency(self, freq):
        """
        Set the minimum number of documents in which a suggestion should appear
        @param freq: Defaults to 0. If the value is greater than 1, it must be a whole number.
        @type freq: int or float
        @return:
        @rtype: self
        """
        return self.set_param("min_doc_freq", freq)

    def set_max_term_frequency(self, freq):
        """
        Set the maximum number of documents in which a suggest text token can exist in order to be included
        @param freq:
        @type freq: float or int
        @return:
        @rtype: self
        """
        return self.set_param("max_term_freq", freq)