import os
import re

import easysparql
from __init__ import RAW_ENDPOINT

import numpy as np
import pandas as pd


def get_features(col):
    """
    :param col:
    :return:
    """
    # Since we are using only have one feature which is the number it self, we append the same column
    # It will results in two identical features, which would help us in the visualization
    return np.append(col, col, 1)


###############################################################
#                   Class/Property Related                    #
###############################################################


def class_property_string_representation(class_uri, property_uri):
    return class_uri + " - " + property_uri


def data_and_meta_from_class_property_uris(class_property_uris=[]):
    """
    get data and meta data from given classes and properties
    a single meta data contains the following: type, from_index and to_index
    :param class_property_uris: a list or triples, each triple is composed of two values, class and property
    :return: data, meta data
    """
    print "\n*********************************************"
    print "*   data_and_meta_from_class_property_uris  *"
    print "*********************************************\n"
    cols = []
    meta_data = []
    meta_start_idx = 0
    #for class_uri, propert_uri in class_property_uris:
    for idx, c_p_uri in enumerate(class_property_uris):
        class_uri, propert_uri = c_p_uri
        print "--------------- extraction ------------------------"
        print "combination: %d" % idx
        print "class: %s" % class_uri
        print "property: %s" % propert_uri
        col = easysparql.get_objects_as_list(endpoint=RAW_ENDPOINT, class_uri=class_uri, property_uri=propert_uri)
        if col.shape != (0, 0):
            cols.append(col)
            single_meta = {}
            single_meta["type"] = class_property_string_representation(class_uri, propert_uri)
            single_meta["from_index"] = meta_start_idx
            meta_start_idx += col.shape[0]
            single_meta["to_index"] = meta_start_idx-1
            meta_data.append(single_meta)

    if len(cols) > 0:
        data = np.array([])
        data.shape = (0, cols[0].shape[1])
        for col in cols:
            data = np.append(data, col, axis=0)
        data = get_features(data)
        return data, meta_data
    else:
        return None, None


###############################################################
#                     CSV Files Related                       #
###############################################################


def data_and_meta_from_files(files):
    """
    To be implemented
    :param files: each file should have a single column
    :return:
    """
    meta_data = []
    meta_start_idx = 0
    data = np.array([])
    data.shape = (0, 1)
    for fname in files:
        col = pd.read_csv("local_data/" + fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname],
                          dtype=np.float64).as_matrix()
        if col.shape[0] == 0:
            continue
        single_meta = {}
        single_meta["type"] = fname
        single_meta["from_index"] = meta_start_idx
        meta_start_idx += col.shape[0]
        single_meta["to_index"] = meta_start_idx - 1
        meta_data.append(single_meta)
        data = np.append(data, col, axis=0)
    data = get_features(data)
    return data, meta_data


###############################################################
#               Save Class/Property to a CSV file             #
###############################################################

# to be implemented
def save_data_and_meta_to_files(data=None, meta_data=None, destination_folder="local_data"):
    if data is None:
        print "save_data_and_meta_to_files> data should not be None"
        return
    if meta_data is None:
        print "save_data_and_meta_to_files> meta_data should not be None"
        return
    for md in meta_data:
        data_sub = data[md["from_index"]:md["to_index"]]
        file_name = md["type"]
        # if file_name[0:5] == "https":
        #     file_name = file_name[5:]
        # elif file_name[0:4] == "http":
        #     file_name = file_name[4:]
        # source: http://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
        file_name = re.sub('[^A-Za-z0-9]+', '_', file_name).strip()
        np.savetxt(os.path.join(destination_folder, file_name), data_sub[:,0], delimiter=",", fmt='%1.5f')































