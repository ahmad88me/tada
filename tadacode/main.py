from __init__ import RAW_ENDPOINT
import data_manipulation
import data_extraction
import learning
import easysparql
import numpy as np
# To print np array without the e (scientific notation)
np.set_printoptions(suppress=True)

def main():
    class_property_combinations = [
        ('http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/numberOfMatches'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longew'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latns'),
        ('http://schema.org/Place', 'http://www.georss.org/georss/point'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]
    class_property_combinations_test = [
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]

    data1, meta_data1 = data_extraction.data_and_meta_from_class_property_uris(class_property_combinations)
    data2, meta_data2 = data_extraction.data_and_meta_from_files(['novHighC.csv'])
    data, meta_data = data_manipulation.merge_data_and_meta_naive(data1=data1, meta_data1=meta_data1, data2=data2,
                                                                  meta_data2=meta_data2)
    for clus, md in enumerate(meta_data):
        print "cluster %d => type: %s" % (clus, md["type"])
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)

    test_data1, test_meta_data1 = data_extraction.data_and_meta_from_class_property_uris(
        class_property_combinations_test)

    test_data2, test_meta_data2 = data_extraction.data_and_meta_from_files(['mayHighC.csv'])
    # merge the two data sets
    test_data, test_meta_data = data_manipulation.merge_data_and_meta_naive(
        data1=test_data1, meta_data1=test_meta_data1, data2=test_data2, meta_data2=test_meta_data2)

    # test_meta_data_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=test_meta_data)
    # learning.test_with_data_and_meta(model=model, data=test_data, meta_data=test_meta_data_with_clusters)
    learning.predict(model=model, data=test_data, meta_data=test_meta_data)


def main_with_class_explore():
    class_uri = 'http://dbpedia.org/ontology/Person'
    properties = easysparql.get_numerical_properties_for_class(endpoint=RAW_ENDPOINT, class_uri=class_uri)
    if properties is None:
        return
    class_property_combinations = zip((len(properties) * [class_uri]), properties)
    print class_property_combinations
    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
        class_property_uris=class_property_combinations)
    # data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)


def main_with_explore():
    classes_properties_uris = easysparql.get_all_classes_properties_numerical(RAW_ENDPOINT)
    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(class_property_uris=classes_properties_uris)
    #data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    #print "model num_of_clusters: %d" % model.n_clusters
    #print "cluster centers: %s" % str(model.cluster_centers_)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)
















# main()
# main_with_class_explore()
main_with_explore()







