from SPARQLWrapper import SPARQLWrapper, JSON


def run_query_with_datatype(query="", endpoint="http://dbpedia.org/sparql",
                            datatype=None):
    """
    :param query: raw SPARQL query
    :param endpoint: endpoint source that hosts the data
    :param datatype: e.g. "http://dbpedia.org/datatype/centimetre"
    :return: 
    """


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
    except Exception as e:
        print "sparql error: $$<%s>$$" % str(e)
        print "query: $$<%s>$$" % str(query)
        return None
    if len(results["results"]["bindings"]) > 0:
        # keys = results["results"]["bindings"][0].keys()
        return results["results"]["bindings"]
    else:
        print "returns 0 rows"
        None

if __name__ == "__main__":
    q = """select ?s ?o where{?s a <http://dbpedia.org/ontology/Person>. ?s <http://dbpedia.org/ontology/Person/height> ?o}
    """
    endpoint = "http://dbpedia.org/sparql"
    run(query=q, endpoint=endpoint)

