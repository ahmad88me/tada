import numpy as np

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
    cols = []
    meta_data = []
    meta_start_idx = 0
    for class_uri, propert_uri in class_property_uris:
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

    return data, meta_data



