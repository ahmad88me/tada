

import data_extraction
import learning


def main():
    class_property_combinations = [
        ('http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/numberOfMatches'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longew'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latns'),
        ('http://schema.org/Place', 'http://www.georss.org/georss/point'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]
    class_property_combinations_test = [
        ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]

    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(class_property_combinations)
    #model = learning.train_with_meta(meta_data=meta_data, num_of_rows=data.shape[0])
    model = learning.train_using_data_and_meta(data=data, meta_data=meta_data)

    test_data, test_meta_data = data_extraction.data_and_meta_from_class_property_uris(class_property_combinations_test)


main()
