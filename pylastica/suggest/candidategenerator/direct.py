__author__ = 'Joe Linn'

from .abstract import AbstractCandidateGenerator


class DirectGenerator(AbstractCandidateGenerator):
    """
    @see: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-suggesters-phrase.html#_direct_generators
    """
    SUGGEST_MODE_MISSING = 'missing'
    SUGGEST_MODE_POPULAR = 'popular'
    SUGGEST_MODE_ALWAYS = 'always'

    def __init__(self, field):
        """

        @param field:
        @type field: str
        """
        super(DirectGenerator, self).__init__()
        self.set_field(field)

    def set_field(self, field):
        """
        Set the field name from which to fetch candidate suggestions
        @param field:
        @type field: str
        @return:
        @rtype: self
        """
        return self.set_param("field", field)

    def set_size(self, size):
        """
        Set the maximum corrections to be returned per suggest text token
        @param size:
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param("size", size)

    def set_suggest_mode(self, mode):
        """

        @param mode: see SUGGEST_MODE_* constants for options
        @type mode: str
        @return:
        @rtype: self
        """
        return self.set_param("suggest_mode", mode)

    def set_max_edits(self, max_edits):
        """

        @param max_edits: can only be a value between 1 and 2. Defaults to 2.
        @type max_edits: float
        @return:
        @rtype: self
        """
        return self.set_param("max_edits", max_edits)

    def set_prefix_length(self, length):
        """

        @param length: defaults to 1
        @type length: int
        @return:
        @rtype: self
        """
        return self.set_param("prefix_len", length)

    def set_min_word_length(self, min_length):
        """

        @param min_length: defaults to 4
        @type min_length: int
        @return:
        @rtype: self
        """
        return self.set_param("min_word_len", min_length)

    def set_max_inspections(self, max_inspections):
        """

        @param max_inspections:
        @type max_inspections: int
        @return:
        @rtype: self
        """
        return self.set_param("max_inspections", max_inspections)

    def set_min_doc_frequency(self, min_frequency):
        """

        @param min_frequency:
        @type min_frequency: float
        @return:
        @rtype: self
        """
        return self.set_param("min_doc_freq", min_frequency)

    def set_max_term_frequency(self, max_frequency):
        """

        @param max_frequency:
        @type max_frequency: float
        @return:
        @rtype: self
        """
        return self.set_param("max_term_freq", max_frequency)

    def set_pre_filter(self, pre):
        """
        Set an analyzer to be applied to the original token prior to candidate generation
        @param pre: an analyzer
        @type pre: str
        @return:
        @rtype: self
        """
        return self.set_param("pre_filter", pre)

    def set_post_filter(self, post):
        """
        Set an analyzer to be applied to generated tokens before they are passed to the phrase scorer
        @param post:
        @type post: str
        @return:
        @rtype: self
        """
        return self.set_param("post_filter", post)