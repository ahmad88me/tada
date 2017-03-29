from SPARQLWrapper import SPARQLWrapper, JSON

from __init__ import QUERY_LIMIT

import pandas as pd
import numpy as np


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
    if endpoint is None:
        print "endpoints cannot be None"
        return []
    sparql = SPARQLWrapper(endpoint=endpoint)
    sparql.setQuery(query=query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            return results["results"]["bindings"]
        else:
            print "returns 0 rows"
            print "endpoint: "+endpoint
            print "query: <%s>" % str(query).strip()
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
    # The below three lines are replaced with the function get_url_stripped
    # class_uri_stripped = class_uri.strip()
    # if class_uri_stripped[0] == "<" and class_uri_stripped[-1] == ">":
    #     class_uri_stripped = class_uri_stripped[1:-1]
    class_uri_stripped = get_url_stripped(class_uri)
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
        %s
    """ % (class_uri_stripped, min_count, QUERY_LIMIT)
    properties = run_query(query=query, endpoint=endpoint)
    return properties


def get_properties_as_list(endpoint=None, class_uri=None, min_count=20):
    properties = get_properties(endpoint=endpoint, class_uri=class_uri, min_count=min_count)
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
        select ?o where{ ?s  a <%s>. ?s <%s> ?o FILTER(isNumeric(?o))} %s
    """ % (class_uri_stripped, property_uri_stripped, QUERY_LIMIT)
    objects = run_query(query=query, endpoint=endpoint)
    return objects


def get_objects_as_list(endpoint=None, class_uri=None, property_uri=None):
    objects = get_objects(endpoint=endpoint, class_uri=class_uri, property_uri=property_uri)
    clean_objects = [o['o'] for o in objects]
    if len(clean_objects) == 0:
        print "no objects found for class %s property %s in endpoint %s" % (class_uri, property_uri, endpoint)
        col_mat = pd.DataFrame([]).as_matrix()
        col_mat.shape = (0, 0)
        #return pd.DataFrame([])
        return col_mat

    col_mat = pd.DataFrame(clean_objects)['value'].as_matrix()
    col_mat.shape = (col_mat.shape[0], 1)
    col_mat = col_mat.astype(np.float)
    #return pd.DataFrame(clean_objects)['value']
    # remove nan is any source: http://stackoverflow.com/questions/11620914/removing-nan-values-from-an-array
    #print "get_objects_as_list> old shape: %s" % str(col_mat.shape)
    col_mat = col_mat[~np.isnan(col_mat)]
    #print "get_objects_as_list> new shape: %s" % str(col_mat.shape)
    col_mat.shape = (col_mat.shape[0], 1)
    #print "get_objects_as_list> new shape after fix: %s" % str(col_mat.shape)
    return col_mat


# # not tested yet
# def objects_to_csv(dest="local_data/output.csv", endpoint=None, class_uri=None, property_uri=None):
#     objects = get_objects_as_list(endpoint=endpoint, class_uri=class_uri, property_uri=property_uri)
#     s = ",\n".join(objects)
#     f = open(dest, 'w')
#     f.write(s)
#     f.close()


def get_numerical_properties_for_class(endpoint=None, class_uri=None):
    """
    get all numerical properties for a given class
    :param endpoint: endpoint
    :param class_uri: class uri for the class
    :return:
    """
    if class_uri is None:
        print "get_numerical_properties_for_class> class_uri should not be None"
        return []
    class_uri_stripped = get_url_stripped(class_uri)
    query = """
    select distinct ?pt where{
    ?pt rdfs:domain <%s>.
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#float>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#double>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#decimal>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#integer>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#nonPositiveInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#negativeInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#long>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#int>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#short>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#byte>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#nonNegativeInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedLong>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedInt>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedShort>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedByte>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#positiveInteger>}
    }
    """ % class_uri_stripped
    results = run_query(query=query, endpoint=endpoint)
    properties = [r['pt']['value'] for r in results]
    return properties


def get_all_classes_properties_numerical(endpoint=None):
    """
    search for all class/property combinations with numerical objects. here we are relying on the defined
    structure using rdfs:range and rdfs:domain and not on the data level
    :param endpoint:
    :return:
    """
    if endpoint is None:
        print "get_all_classes_properties_numerical> endpoint should not be None"
        return []
    query = """
    select distinct ?pt ?c where{
    ?pt rdfs:domain ?c.
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#float>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#double>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#decimal>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#integer>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#nonPositiveInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#negativeInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#long>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#int>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#short>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#byte>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#nonNegativeInteger>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedLong>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedInt>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedShort>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#unsignedByte>} UNION
    {?pt rdfs:range <http://www.w3.org/2001/XMLSchema#positiveInteger>}
    }
    """
    results = run_query(query=query, endpoint=endpoint)
    class_property_uris = [(r['c']['value'], r['pt']['value']) for r in results]
    return class_property_uris


def get_url_stripped(uri):
    """
    :param uri:  <myuri> or uri
    :return: myuri
    """
    uri_stripped = uri.strip()
    if uri_stripped[0] == "<":
        uri_stripped = uri_stripped[1:]
    if uri_stripped[-1] == ">":
        uri_stripped = uri_stripped[:-1]
    return uri_stripped










