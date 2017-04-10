import os
import re
import math

import easysparql

import numpy as np
import pandas as pd
import random
import string


def get_features(col):
    """
    :param col:
    :return:
    """
    # Since we are using only have one feature which is the number it self, we append the same column
    # It will results in two identical features, which would help us in the visualization
    return np.append(col, col, 1)


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))

###############################################################
#                   Class/Property Related                    #
###############################################################


def class_property_string_representation(class_uri, property_uri):
    return class_uri + " - " + property_uri


def data_and_meta_from_class_property_uris(endpoint=None, class_property_uris=[], update_func=None, isnumericfilter=True):
    """
    get data and meta data from given classes and properties
    a single meta data contains the following: type, from_index and to_index
    :param class_property_uris: a list or triples, each triple is composed of two values, class and property
    :return: data, meta data
    """
    print "\n*********************************************"
    print "*   data_and_meta_from_class_property_uris  *"
    print "*********************************************\n"
    if endpoint is None:
        print "data_and_meta_from_class_property_uris> endpoint should not be None"
        return None, None
    cols = []
    meta_data = []
    meta_start_idx = 0
    num_of_uris = len(class_property_uris)

    if update_func is None:
        for idx, c_p_uri in enumerate(class_property_uris):
            class_uri, propert_uri = c_p_uri
            print "--------------- extraction ------------------------"
            print "combination: %d" % idx
            print "class: %s" % class_uri
            print "property: %s" % propert_uri
            col = easysparql.get_objects_as_list(endpoint=endpoint, class_uri=class_uri, property_uri=propert_uri,
                                                 isnumericfilter=isnumericfilter)
            if col.shape[0] != 0:
            #if col.shape != (0, 0):
                cols.append(col)
                single_meta = {}
                single_meta["type"] = class_property_string_representation(class_uri, propert_uri)
                single_meta["from_index"] = meta_start_idx
                meta_start_idx += col.shape[0]
                # single_meta["to_index"] = meta_start_idx-1
                single_meta["to_index"] = meta_start_idx
                meta_data.append(single_meta)
    else:
        for idx, c_p_uri in enumerate(class_property_uris):
            class_uri, propert_uri = c_p_uri
            print "--------------- extraction ------------------------"
            print "combination: %d" % idx
            print "class: %s" % class_uri
            print "property: %s" % propert_uri
            col = easysparql.get_objects_as_list(endpoint=endpoint, class_uri=class_uri, property_uri=propert_uri,
                                                 isnumericfilter=isnumericfilter)
            # print "debug: extraction col"
            # print 'col.shape %s' % str(col.shape)
            if col.shape[0] != 0:
            #if col.shape != (0, 0):
                cols.append(col)
                single_meta = {}
                single_meta["type"] = class_property_string_representation(class_uri, propert_uri)
                single_meta["from_index"] = meta_start_idx
                meta_start_idx += col.shape[0]
                # single_meta["to_index"] = meta_start_idx-1
                single_meta["to_index"] = meta_start_idx
                meta_data.append(single_meta)
                update_func(int(idx*1.0/num_of_uris * 100))

    if update_func is not None:
        update_func(100)

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
        #single_meta["to_index"] = meta_start_idx - 1
        single_meta["to_index"] = meta_start_idx
        meta_data.append(single_meta)
        data = np.append(data, col, axis=0)
    data = get_features(data)
    return data, meta_data


def data_and_meta_from_a_mixed_file(file_name=None, original_file_name=None, has_header=False):
    """
    Currently only used by core.py for the web ui
    :param file_name: the file can have multiple columns, numerical and non-numericals, but should not have a header
    :param original_file_name: the original file name, it will be used in the type in the meta
    :return: data and meta

    """
    if file_name is None:
        print "data_and_meta_from_a_mixed_file> file_name should not be None"
        return None, None
    if original_file_name is None:
        print "data_and_meta_from_a_mixed_file> original_file_name should not be None"
        return None, None
    if has_header:
        df = pd.read_csv(file_name, error_bad_lines=False, warn_bad_lines=False, skip_blank_lines=True)
    else:
        df = pd.read_csv(file_name, header=None, error_bad_lines=False, warn_bad_lines=False, skip_blank_lines=True)
    # num_cols = df.select_dtypes(include=[np.float, np.int]).as_matrix().astype(np.float64)
    meta_data = []
    meta_start_idx = 0
    data = np.array([])
    data.shape = (0, 1)
    data_list = []
    for col_idx, col_name in enumerate(df.columns):
        if df[col_name].dtype == np.int or df[col_name].dtype == np.float:
            col = df[col_name].as_matrix()
            col.shape = (col.shape[0], 1)
        else:
            continue
        if col.shape[0] == 0:
            continue

        # compute the type
        #the_type = file_name.split('/')[-1].strip()
        the_type = original_file_name
        # if the_type[-4:].lower() == '.csv':
        #     the_type = the_type[:-4]
        the_type = the_type + " , " + str(col_idx)

        single_meta = {}
        single_meta["type"] = the_type
        single_meta["from_index"] = meta_start_idx
        meta_start_idx += col.shape[0]
        single_meta["to_index"] = meta_start_idx
        meta_data.append(single_meta)
        # print "data shape is:"
        # print data.shape
        # print "data is: "
        # print data
        # print "col shape is:"
        # print col.shape
        # print "col is:"
        # print col
        # Changing the shape for the col so it can be appended to the data
        col.shape = (col.shape[0], 1)
        # print "changed col shape is:"
        # print col.shape
        # print "changed col is:"
        # print col
        data = np.append(data, col, axis=0)
        #data_list += col
    #data = np.array(data_list)
    data = get_features(data)
    print "data_and_meta_from_a_mixed_file> data shape %s" % str(data.shape)
    return data, meta_data


###############################################################
#               Save Class/Property to a CSV file             #
###############################################################

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


##################################################
#            Extracting Data models              #
##################################################

def save_model(model=None, meta_data=None, file_name=None):
    """
    :param model: FCM model
    :param file_name: string to be a prefix for the actual name
    :return: new_file_name or None if failed to save the model
    """
    if model is None:
        print "save_model> model should not be empty"
        return None
    if meta_data is None:
        print "save_model> meta_data should not be empty"
        return None
    # just in case it was not np array
    centers = np.array(model.cluster_centers_)
    fname = random_string()+'.csv'
    if file_name is not None:
        fname = file_name + fname
    f = open(os.path.join('local_models', fname), 'w')
    for idx, c in enumerate(centers):
        #f.write(",".join([str(cc) for cc in c]))
        f.write(",".join(["%1.5f" % cc for cc in c]))
        f.write(","+meta_data[idx]["type"])
        f.write("\n")
    f.close()
    return fname
































