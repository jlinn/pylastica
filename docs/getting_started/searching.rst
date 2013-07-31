.. _searching:

Searching
=========

Querying
--------

Each of the Elasticsearch query types is represented as an object in pylastica. These can be found in pylastica's query module.
The following example demonstrates the use of a `query string <http://www.elasticsearch.org/guide/reference/query-dsl/query-string-query/>`_ query:

.. code-block:: python

    # instantiate the query object
    pylastica_query_string = pylastica.query.QueryString()

    # set the query parameters
    pylastica_query_string.set_default_operator('AND')
    pylastica_query_string.set_query('thomas anderson')

    # perform the search
    pylastica_result_set = pylastica_index.search(pylastica_query_string)

Pagination of search results can be implemented like so:

.. code-block:: python

    # create a generic Query object using the StringQuery object
    pylastica_query = pylastica.query.Query(pylastica_query_string)

    # set pagination parameters
    pylastica_query.set_from(50)    # start at the 50th result
    pylastica_query.set_limit(25)   # return 25 results

    # perform the search, this time using the Query object which wraps the QueryString object
    pylastica_result_set = pylastica_index.search(pylastica_query)

Retrieving Results
------------------

.. code-block:: python

    # extract the actual results from the result set
    pylastica_results = pylastica_result_set.results

    # get the total number of results
    total_results = pylastica_result_set.get_total_hits()

    # iterate over the results
    for result in pylastica_results:
        result_data = result.data
        # do something with the data

Filtering
---------

As with queries, each Elasticsearch filter type is represented as an object in pylastica's filter module.
The following example illustrates combining two `term filters <http://www.elasticsearch.org/guide/reference/query-dsl/term-filter/>`_ using an `or filter <http://www.elasticsearch.org/guide/reference/query-dsl/or-filter/>`_:

.. code-block:: python

    # filter for the name "neo"
    pylastica_filter_name_neo = pylastica.filter.Term('name', 'neo')

    pylastica_filter_name_trinity = pylastica.filter.Term('name', 'trinity')

    # filter for either "neo" or "trinity"
    pylastica_filter_or = pylastica.filter.BoolOr()
    pylastica_filter_or.add_filter(pylastica_filter_name_neo)
    pylastica_filter_or.add_filter(pylastica_filter_name_trinity)

    # add the filter to the Query object
    pylastica_query.set_filter(pylastica_filter_or)

Facets
------

The trend of Elasticsearch query constructs represented as objects continues with pylastica's `facet <http://www.elasticsearch.org/guide/reference/api/search/facets/>`_ implementation.
Here is an example using a `terms facet <http://www.elasticsearch.org/guide/reference/api/search/facets/terms-facet/>`_:

.. code-block:: python

    # define a facet
    pylastica_facet = pylastica.facet.Terms('facet_name')   # instantiate the Facet object, giving the facet a name
    pylastica_facet.set_field('name')
    pylastica_facet.set_size(10)
    pylastica_facet.set_order('reverse_count')

    # add the facet to the Query object
    pylastica_query.add_facet(pylastica_facet)

The above facet will return the 10 least frequently occurring values in the "name" field, along with the count for each value, in order of ascending frequency.
Retrieving facet data works as follows:

.. code-block:: python

    facets = pylastica_result_set.get_facets()
    for facet in facets['facet_name']['terms']:
        term = facet['term']    # the value
        count = facet['count']  # the count
