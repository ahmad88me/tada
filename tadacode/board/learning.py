
import numpy as np

from clustering.fuzzy_clustering import FCM


def train_with_data_and_meta(data=None, meta_data=None):
    """
    :param data: data points
    :param meta_data: a list of meta_data, each meta_data is a dict
    :return: FCM model
    """
    if meta_data is None:
        print "train_with_data_and_meta> meta data can't be None"
        return None
    if data is None:
        print "train_with_data_and_meta> data can't be None"
        return None
    model = FCM(n_clusters=len(meta_data), max_iter=1)
    u = np.zeros((data.shape[0], len(meta_data)))
    for clus, md in enumerate(meta_data):
        print "%d from index %d to index %d" % (clus, md["from_index"], md["to_index"])
        for i in range(md["from_index"], md["to_index"]+1):
            u[i][clus] = 1.0
    model.u = u
    model.compute_cluster_centers(data)
    return model


# def test_with_data_and_meta(model=None, data=None, meta_data=None):
#     if model is None:
#         print "test_with_data_and_meta> model should not be None"
#     if data is None:
#         print "test_with_data_and_meta> data should not be None"
#     if meta_data is None:
#         print "test_with_data_and_meta> meta_data should not be None"




# The below is no longer valid because cluster centers can't be computed without the data it self
# def train_with_meta(meta_data=None, num_of_rows=0):
#     """
#     :param num_of_rows: can be obtained data.shape[0]
#     :param meta_data: a list of meta_data, each meta_data is a dict
#     :return: FCM model
#     """
#     # it was only the below three lines without the data argument as well
#     # model = FCM(n_clusters=n_clusters, max_iter=max_iter, m=m)
#     # model.cluster_centers_ = centroids
#     # return model
#     if meta_data is None:
#         print "train> meta data can't be None"
#         return None
#     model = FCM(n_clusters=len(meta_data), max_iter=1)
#     u = np.zeros((num_of_rows, len(meta_data)))
#     for clus, md in enumerate(meta_data):
#         print "%d from index %d to index %d" % (clus, md["from_index"], md["to_index"])
#         for i in range(md["from_index"], md["to_index"]+1):
#             u[i][clus] = 1.0
#     model.u = u
#     return model
