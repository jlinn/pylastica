__author__ = 'Joe Linn'

from .abstract import AbstractSuggestion


class Phrase(AbstractSuggestion):
    """
    @see: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-suggesters-phrase.html
    """

    def set_analyzer(self, analyzer):
        """
        Set the analyzer for this suggestion
        @param analyzer: a pre-defined Elasticsearch analyzer
        @type analyzer: str
        @return:
        @rtype: self
        """
        return self.set_param("analyzer", analyzer)

    def set_gram_size(self, size):
        """
        Set the max size of the n-grams (shingles) in the field
        @param size:
        @type size: int
        @return:
        @rtype: self
        """
        return self.set_param("gram_size", size)

    def set_real_world_error_likelihood(self, likelihood):
        """
        Set the likelihood of a term being misspelled even if the term exists in the dictionary
        @param likelihood: Defaults to 0.95, meaning 5% of the words are misspelled.
        @type likelihood: float
        @return:
        @rtype: self
        """
        return self.set_param("real_world_error_likelihood", likelihood)

    def set_confidence(self, confidence):
        """
        Set the factor applied to the input phrases score to be used as a threshold for other suggestion candidates.
        Only candidates which score higher than this threshold will be included in the result.
        @param confidence: Defaults to 1.0
        @type confidence: float
        @return:
        @rtype: self
        """
        return self.set_param("confidence", confidence)

    def set_max_errors(self, max_errors):
        """
        Set the maximum percentage of the terms considered to be misspellings in order to form a correction
        @param max_errors:
        @type max_errors: float
        @return:
        @rtype: self
        """
        return self.set_param("max_errors", max_errors)

    def set_separator(self, separator):
        """

        @param separator:
        @type separator: str
        @return:
        @rtype: self
        """
        return self.set_param("separator", separator)

    def set_highlight(self, pre_tag, post_tag):
        """
        Set suggestion highlighting
        @param pre_tag:
        @type pre_tag: str
        @param post_tag:
        @type post_tag: str
        @return:
        @rtype: self
        """
        return self.set_param("highlight", {
            'pre_tag': pre_tag,
            'post_tag': post_tag
        })

    def set_stupid_backoff_smoothing(self, discount = 0.4):
        """

        @param discount:
        @type discount: float
        @return:
        @rtype: self
        """
        return self.set_smoothing_model("stupid_backoff", {"discount": discount})

    def set_laplace_smoothing(self, alpha=0.5):
        """

        @param alpha:
        @type alpha: float
        @return:
        @rtype: self
        """
        return self.set_smoothing_model("laplace", {"alpha": alpha})

    def set_linear_interpolation_smoothing(self, trigram_lambda, bigram_lambda, unigram_lambda):
        """

        @param trigram_lambda:
        @type trigram_lambda: float
        @param bigram_lambda:
        @type bigram_lambda: float
        @param unigram_lambda:
        @type unigram_lambda: float
        @return:
        @rtype: self
        """
        return self.set_smoothing_model("linear_interpolation", {
            "trigram_lambda": trigram_lambda,
            "bigram_lambda": bigram_lambda,
            "unigram_lambda": unigram_lambda
        })

    def set_smoothing_model(self, model, params):
        """

        @param model: the name of the smoothing model
        @type model: str
        @param params:
        @type params: dict
        @return:
        @rtype: self
        """
        return self.set_param("smoothing", {model: params})

    def add_candidate_generator(self, generator):
        """

        @param generator:
        @type generator: pylastica.suggest.candidategenerator.abstract.AbstractCandidateGenerator
        @return:
        @rtype: self
        """
        generator = generator.to_dict()
        return self.add_param(generator.keys()[0], generator.values()[0])