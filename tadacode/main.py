
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as matplot_colors
import six

from clustering.fuzzy_clustering import FCM


def compute_centroids(X, n_clusters, labels, distances):
    n_samples = X.shape[0]
    n_features = X.shape[1]
    new_centers = np.zeros((n_clusters, n_features))
    n_samples_in_cluster = np.bincount(labels, minlength=n_clusters)
    empty_clusters = np.where(n_samples_in_cluster == 0)[0]

    # This is to assign values to empty_clusters
    if len(empty_clusters):
        # find points to reassign empty clusters to
        far_from_centers = distances.argsort()[::-1]

        for i, cluster_id in enumerate(empty_clusters):
            # XXX two relocated clusters could be close to each other
            new_center_point = X[far_from_centers[i]]
            new_centers[cluster_id] = new_center_point
            n_samples_in_cluster[cluster_id] = 1
    # for each cluster, sum the values of the same axis (e.g. sum the x's together, the y's together ,and the z's)
    for i in range(n_samples):
        for j in range(n_features):
            new_centers[labels[i], j] += X[i, j]

    # Take the average for of the sum calculated in the above loop
    new_centers /= n_samples_in_cluster[:, np.newaxis]
    return new_centers


def explore_single_column(col, color):
    plt.scatter(col, col, c=color)


def data_exploration():
    files = ["code_postal.csv", "mayHighC.csv"]
    colors = list(six.iteritems(matplot_colors.cnames))
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/"+fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname], dtype=np.float64)
        explore_single_column(col, colors[idx])
    plt.show()

data_exploration()

## Next steps
# Compute the centriods

