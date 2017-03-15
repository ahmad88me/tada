from SPARQLWrapper import SPARQLWrapper, JSON

import pandas as pd


def run_query_with_datatype(query=None, endpoint=None, datatype=None):
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


def run_query(query=None, endpoint=None):
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


def get_properties(endpoint=None, class_uri=None, min_count=20):
    """
    :param endpoint: the meta endpoint
    :param class_uri: with or without < and >
    :param min_count:
    :return: returns the properties and can be accessed as follows: properties[idx]['property']['value']
    """
    class_uri_stripped = class_uri.strip()
    if class_uri_stripped[0] == "<" and class_uri_stripped[-1] == ">":
        class_uri_stripped = class_uri_stripped[1:-1]
    # query = """
    #     prefix loupe: <http://ont-loupe.linkeddata.es/def/core/>
    #     prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    #     select ?p ?count where {
    #       graph <http://data.loupe.linked.es/dbpedia/1> {
    #         ?pp loupe:aboutClass <%s>;
    #             loupe:aboutProperty ?p;
    #             loupe:hasDatatypePartition ?pdp .
    #         ?pdp loupe:datatype xsd:double;
    #             loupe:objectCount ?count .
    #      }
    #     }
    #     ORDER BY desc(?count)
    # """ % class_uri_stripped
    query = """
    prefix loupe: <http://ont-loupe.linkeddata.es/def/core/>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        select distinct ?p as ?property ?count where {
          graph <http://data.loupe.linked.es/dbpedia/1> {
            ?pp loupe:aboutClass <%s>;
                loupe:aboutProperty ?p;
                loupe:hasDatatypePartition ?pdp;
                loupe:objectCount ?count .
            {
            ?pdp loupe:datatype xsd:double .
            } UNION {
            ?pdp loupe:datatype xsd:integer .
            } UNION {
            ?pdp loupe:datatype xsd:decimal .
            }
           FILTER(?count > %d)
         }
        }
        ORDER BY desc(?count)
    """ % (class_uri_stripped, min_count)
    properties = run_query(query=query, endpoint=endpoint)
    return properties


def get_properties_as_list(endpoint=None, class_uri=None, min_count=20):
    properties = get_properties(class_uri=class_uri, min_count=min_count)
    clean_properties = [p['property'] for p in properties]
    return pd.DataFrame(clean_properties)['value']


def get_objects(endpoint=None, class_uri=None, property_uri= None):
    class_uri_stripped = class_uri.strip()
    if class_uri_stripped[0] == "<" and class_uri_stripped[-1] == ">":
        class_uri_stripped = class_uri_stripped[1:-1]
    property_uri_stripped = property_uri.strip()
    if property_uri_stripped[0] == "<" and property_uri_stripped[-1] == ">":
        property_uri_stripped = property_uri_stripped[1:-1]
    query = """
        select ?o where{ <%s> <%s> ?o}
    """ % (class_uri_stripped, property_uri_stripped)
    objects = run_query(query=query, endpoint=endpoint)
    return objects


def get_objects_as_list(endpoint=None, class_uri=None, property_uri= None):
    objects = get_objects(endpoint=endpoint, class_uri=class_uri, property_uri=property_uri)
    clean_objects = [o['o'] for o in objects]
    return pd.DataFrame(clean_objects)['value']
