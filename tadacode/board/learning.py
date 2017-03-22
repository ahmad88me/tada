import __init__

from __init__ import RAW_ENDPOINT, META_ENDPOINT

import numpy as np
import pandas as pd

from clustering.fuzzy_clustering import FCM

from easysparql import get_properties_as_list, get_objects_as_list

import easysparql

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)


def compute_centroid_single_cluster(X):
    """
    :param X: numpy array
    :return: center point of the X
    """
    n_samples = X.shape[0]
    n_features = X.shape[1]
    new_center = np.zeros((1, n_features))
    # for each cluster, sum the values of the same axis (e.g. sum the x's together, the y's together ,and the z's)
    for i in range(n_samples):
        for j in range(n_features):
            new_center[0, j] += X[i, j]
    # Take the average for of the sum calculated in the above loop
    new_center /= X.shape[0]
    return new_center[0]


def get_features(col):
    # Since we are using only have one feature which is the number it self, we append the same column
    # It will results in two identical features, which would help us in the visualization
    # col = np.append(col, col, 1)
    # print "get_features> type of col is: %s"+str(type(col))
    # print "get_features> col shape %s" % str(col.shape)
    # print col
    return np.append(col, col, 1)


def get_centroids_for_files(files):
    """
    :param files: files each with a single columns
    :return: a list of centroids
    """
    n_features = 2
    centroids = np.array([])
    centroids.shape = (0, n_features)
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/"+fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname],
                          dtype=np.float64).as_matrix()
        col = get_features(col)
        centroid = compute_centroid_single_cluster(col)
        centroids = np.append(centroids, [centroid], axis=0)
    return centroids


def get_centroids_for_lists(cols):
    """
    :param cols:  a list of numpy lists (vectors)
    :return:  a list of centroids
    """
    n_features = 2
    centroids = np.array([])
    centroids.shape = (0, n_features)
    for c in cols:
        col = get_features(c)
        centroid = compute_centroid_single_cluster(col)
        centroids = np.append(centroids, [centroid], axis=0)
    return centroids


def measure_representativeness(model, files):
    """
    This function is meant to measure the representativeness of the training set
    :param model: FCM model
    :param files: a list of file names, each with a single column of numbers
    :return: a list of representativeness (between 0 and 1 each for each file)
    """
    repr = []
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/" + fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname],
                          dtype=np.float64).as_matrix()
        col = get_features(col)
        membership = model.predict(col)
        avg = np.average(membership, axis=0)
        repr.append(avg[idx])
        # median = np.median(membership, axis=0)
        # print "=========\n" + fname
        # print "average membership"
        # print avg
        # print "median membership"
        # print median
    return repr


def get_data_from_files(files):
    n_features = 2
    cols = np.array([])
    cols.shape = (0, n_features)
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/"+fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname],
                          dtype=np.float64).as_matrix()
        col = get_features(col)
        cols = np.append(cols, col, axis=0)
    return cols


def get_data_from_uris(meta_endpoint=None, raw_endpoint=None, class_uris=[], property_min_count=20,
                       top_k_properties_per_class=5):
    n_features = 2
    cols = np.array([])
    cols.shape = (0, n_features)

    for class_uri in class_uris:
        properties = easysparql.get_properties_as_list(endpoint=META_ENDPOINT, class_uri=class_uri,
                                                       min_count=property_min_count)[:top_k_properties_per_class]
        for aproperty in properties:
            col = easysparql.get_objects_as_list(endpoint=RAW_ENDPOINT, class_uri=class_uri, property_uri=aproperty)
            col = get_features(col)
            cols = np.append(cols, col, axis=0)
    return cols


def train(centroids=[], n_clusters=None, max_iter=1, m=2):
    """
    :param centroids: list of cluster centers
    :param n_clusters:
    :param max_iter: by default 1 because centroids are given
    :param m: fuzziness
    :return: FCM model
    """
    model = FCM(n_clusters=n_clusters, max_iter=max_iter, m=m)
    model.cluster_centers_ = centroids
    return model


def train_from_files(training_files):
    """
    This function is responsible for training the model and compute the representative of each file
    :return: FCM model
    """
    centroids = get_centroids_for_files(training_files)
    # print "centroids: "
    # print centroids
    return train(centroids=centroids, n_clusters=len(training_files), max_iter=1, m=2)


def train_from_class_uris(class_uris=[], top_k_properties_per_class=5, min_objects_per_property=20):
    cols = []
    for class_uri in class_uris:
        for property in get_properties_as_list(endpoint=META_ENDPOINT, class_uri=class_uri,
                                               min_count=min_objects_per_property)[: top_k_properties_per_class]:
                col = get_objects_as_list(endpoint=RAW_ENDPOINT, class_uri=class_uri, property_uri=property)
                if col.shape != (0, 0):
                    # col_mat = col.as_matrix()
                    # col_mat.shape = (col_mat.shape[0], 1)
                    # cols.append(col_mat.astype(np.float))
                    cols.append(col)
    # print "will computer centroids for lists"
    # print "%d centers" % len(cols)
    # print "train from class uris> cols:"
    print cols
    centroids = get_centroids_for_lists(cols)
    return train(centroids=centroids, n_clusters=len(cols), max_iter=1, m=2)


def inspect_membership(meta_data, membership):
    """
    :param meta_data: a list of meta objects, each meta object contains the following: class, property, from_index and
    to_index
    :param membership: it is the membership matrix
    :return: nothing
    """
    print "meta data"
    print meta_data
    for clus, md in enumerate(meta_data):
        membership_for_cluster = membership[md["from_index"]: md["to_index"]]
        print "================\n%s - %s: (%d)" % (md["class"], md["property"], clus)
        print " MEAN:  "+str(np.average(membership_for_cluster, axis=0))
        print "MEDIAN: "+str(np.median(membership_for_cluster, axis=0))


def merge_clusters_from_meta(data, meta_data):
    """
    :param data: data points
    :param meta_data: a list of meta objects, each meta object contains the following: class, property,
            alternative(optional), from_index and to_index
    :return: ordered_data, model, new_meta
    """
    new_meta = []
    new_data = np.array([])
    new_data.shape = (0, data.shape[1])
    data_per_cluster = {}
    for clus, md in enumerate(meta_data):
        if "alternative" in md:
            # now check if the alternative cluster does not have an alternative as well
            if "alternative" not in meta_data[md["alternative"]]:
                if md["alternative"] in data_per_cluster:
                    data_per_cluster[md["alternative"]] = np.append(data_per_cluster[md["alternative"]],
                                                                    data[md["from_index"]:md["to_index"]], axis=0)
                else:
                    data_per_cluster[md["alternative"]] = data[md["from_index"]:md["to_index"]]
        else:
            if clus is data_per_cluster:
                data_per_cluster[clus] = np.append(data_per_cluster[clus], data[md["from_index"]:md["to_index"]])
            else:
                data_per_cluster[clus] = data[md["from_index"]:md["to_index"]]
    idx = 0
    for clus in data_per_cluster.keys():
        new_data = np.append(new_data, data_per_cluster[clus], axis=0)
        meta = {}
        meta["from_idx"] = idx
        idx += data_per_cluster[clus].shape[0]
        meta["to_idx"] = idx-1
        meta["class"] = meta_data[clus]["class"]
        meta["property"] = meta_data[clus]["property"]


def compute_representativeness_from_meta(meta_data, membership):
    """
    compute the representativeness for each class/property triple
    :param meta_data: a list of meta objects, each meta object contains the following: class, property, from_index and
    to_index
    :param membership: it is the membership matrix
    :return: nothing
    """
    avg_membership_score = 0.0
    for clus, md in enumerate(meta_data):
        membership_for_cluster = membership[md["from_index"]: md["to_index"]]
        avg = np.average(membership_for_cluster, axis=0)
        max_mem_id = np.argmax(avg)
        print "================\n%s - %s: (%d)" % (md["class"], md["property"], clus)
        print "representativeness: %f" % avg[clus]
        if max_mem_id != clus and avg[max_mem_id] > avg[clus]:  #  the second condition in case there are two clusters
                                                                # with  the same membership
            print "alternative (%d) %s - %s with membership score: %f" % (max_mem_id, meta_data[max_mem_id]["class"],
                                                                     meta_data[max_mem_id]["property"],
                                                                     avg[max_mem_id])
            print " MEAN:  " + str(avg)
            # This is to return the alternative cluster with the meta data
            meta_data[clus]["alternative_cluster"] = max_mem_id
        # the is just to computer the average score totally
        avg_membership_score += avg[clus]
    print "================\n\nMEAN membership score is: %f\n" % (avg_membership_score/len(meta_data))
    return meta_data


def train_from_class_property_uris(class_property_uris=[], get_data=False, get_meta_data=False):
    cols = []
    meta_data_about_cols = []
    meta_start_idx = 0
    for class_uri, propert_uri in class_property_uris:
        col = easysparql.get_objects_as_list(endpoint=RAW_ENDPOINT, class_uri=class_uri, property_uri=propert_uri)
        if col.shape != (0, 0):
            cols.append(col)
            single_meta = {}
            single_meta["class"] = class_uri
            single_meta["property"] = propert_uri
            single_meta["from_index"] = meta_start_idx
            meta_start_idx += col.shape[0]
            single_meta["to_index"] = meta_start_idx-1
            meta_data_about_cols.append(single_meta)
    centroids = get_centroids_for_lists(cols)
    if get_data is False:
        return train(centroids=centroids, n_clusters=len(cols), max_iter=1, m=2)

    if len(cols) > 0:
        print "train_from_class_property_uris> num of clusters: %d" % len(cols)
        data = np.array([])
        data.shape = (0, cols[0].shape[1])
        for col in cols[1:]:
            data = np.append(data, col, axis=0)
        #return train(centroids=centroids, n_clusters=len(cols), max_iter=1, m=2), get_features(np.array(data))
        model = train(centroids=centroids, n_clusters=len(cols), max_iter=1, m=2)
        if get_meta_data:
            return model, get_features(np.array(data)), meta_data_about_cols
        else:
            return model, get_features(np.array(data))
    else:
        print "train_from_class_property_uris> nothing to cluster"
        if get_meta_data:
            return None, None, None
        else:
            return None, None


def test(model, files):
    """
    :param model: FCM model
    :param files: list of files to be used for testing
    :return: membership of the predictions
    """
    memberships = np.array([])
    memberships.shape = (0, len(model.cluster_centers_))
    membership_list = []
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/" + fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname],
                          dtype=np.float64).as_matrix()
        col = get_features(col)
        m = model.predict(col)
        membership_list.append(m)
    for idx, m in enumerate(membership_list):
        print "for file: "+files[idx]
        print "average: "
        print np.average(m, axis=0)
        print "median: "
        print np.median(m, axis=0)
        memberships = np.append(memberships, np.average(m, axis=0), axis=0)
    return memberships

