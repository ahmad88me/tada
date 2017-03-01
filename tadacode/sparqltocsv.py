from SPARQLWrapper import SPARQLWrapper, JSON


def run_query_with_datatype(query="", endpoint="http://dbpedia.org/sparql", datatype=None):
    """
    :param query: raw SPARQL query
    :param endpoint: endpoint source that hosts the data
    :param datatype: e.g. "http://dbpedia.org/datatype/centimetre" if None, it will return all datatypes
    :return: query results with the matching datatype, query results not matching the given datatype
    """
    results = run_query(query=query, endpoint=endpoint)
    if len(results) > 0:
        if len(results[0].keys()) == 1:
            k = results[0].keys()[0]
            if datatype is None:
                correct_type_results = [r[k]["value"] for r in results]
                wrong_type_results = []
            else:
                correct_type_results = [r[k]["value"] for r in results if r[k]["datatype"] == datatype]
                wrong_type_results = [r[k]["value"] for r in results if r[k]["datatype"] != datatype]
            return correct_type_results, wrong_type_results
        else:
            print "a query that results in multiple columns is not allowed"
            # Because, if we allow having multiple columns, and the number of values in the first column
            # that matches the given datatype might not be the same as the one in the second column
            # which would results in unbalanced results
    return [], []


def run_query(query="", endpoint="http://dbpedia.org/sparql"):
    """
    :param query: raw SPARQL query
    :param endpoint: endpoint source that hosts the data
    :return: query result as a dict
    """
    sparql = SPARQLWrapper(endpoint=endpoint)
    sparql.setQuery(query=query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            return results["results"]["bindings"]
        else:
            print "returns 0 rows"
            return []
    except Exception as e:
        print "sparql error: $$<%s>$$" % str(e)
        print "query: $$<%s>$$" % str(query)
        return []


if __name__ == "__main__":
    # q = """select ?s ?o where{?s a <http://dbpedia.org/ontology/Person>. ?s <http://dbpedia.org/ontology/Person/height> ?o}
    # """
    q = """select ?s where{?s a <http://dbpedia.org/ontology/Person>. ?s <http://dbpedia.org/ontology/Person/height> ?o}
    """
    endpoint = "http://dbpedia.org/sparql"
    run_query_with_datatype(query=q, endpoint=endpoint, datatype="")
    #run_query(query=q, endpoint=endpoint)



query = """select ?s where{?s a <http://dbpedia.org/ontology/Person>. ?s <http://dbpedia.org/ontology/Person/height> ?o}
"""
endpoint = "http://dbpedia.org/sparql"
sparql = SPARQLWrapper(endpoint=endpoint)
sparql.setQuery(query=query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
results = results["results"]["bindings"]




