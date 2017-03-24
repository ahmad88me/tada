
from clustering.fuzzy_clustering import FCM

import numpy as np


def train_with_meta(meta_data=None, num_of_rows=0):
    """
    :param num_of_rows: can be obtained data.shape[0]
    :param meta_data: a list of meta_data, each meta_data is a dict
    :return: FCM model
    """
    # it was only the below three lines without the data argument as well
    # model = FCM(n_clusters=n_clusters, max_iter=max_iter, m=m)
    # model.cluster_centers_ = centroids
    # return model
    if meta_data is None:
        print "train> meta data can't be None"
        return None
    model = FCM(n_clusters=len(meta_data), max_iter=1)
    u = np.zeros((num_of_rows, len(meta_data)))
    for clus, md in enumerate(meta_data):
        print "%d from index %d to index %d" % (clus, md["from_index"], md["to_index"])
        for i in range(md["from_index"], md["to_index"]+1):
            u[i][clus] = 1.0
    model.u = u
    return model
