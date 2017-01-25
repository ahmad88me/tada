
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as matplot_colors
import six

from clustering.fuzzy_clustering import FCM


def compute_centroid_single_cluster(X, cluster_id):
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


# def compute_centroids(X, n_clusters, labels, distances):
#     n_samples = X.shape[0]
#     n_features = X.shape[1]
#     new_centers = np.zeros((n_clusters, n_features))
#     n_samples_in_cluster = np.bincount(labels, minlength=n_clusters)
#     empty_clusters = np.where(n_samples_in_cluster == 0)[0]
#
#     # This is to assign values to empty_clusters
#     if len(empty_clusters):
#         # find points to reassign empty clusters to
#         far_from_centers = distances.argsort()[::-1]
#
#         for i, cluster_id in enumerate(empty_clusters):
#             # XXX two relocated clusters could be close to each other
#             new_center_point = X[far_from_centers[i]]
#             new_centers[cluster_id] = new_center_point
#             n_samples_in_cluster[cluster_id] = 1
#     # for each cluster, sum the values of the same axis (e.g. sum the x's together, the y's together ,and the z's)
#     for i in range(n_samples):
#         for j in range(n_features):
#             new_centers[labels[i], j] += X[i, j]
#
#     # Take the average for of the sum calculated in the above loop
#     new_centers /= n_samples_in_cluster[:, np.newaxis]
#     return new_centers


def explore_single_cluster(col, center, color):
    plt.scatter(col, col, c=color, marker="o", s=100, linewidths=0, alpha=0.4)
    plt.scatter([center[0]], [center[1]], c=color, s=500, linewidths=5, marker="x")


# def explore_single_column(col, cluster_id, color, marker):
#     plt.scatter(col, col, c=color, marker=marker, s=100, linewidths=0, alpha=0.4)
#     center = compute_centroid_single_cluster(col, cluster_id)
#     center = center.flatten()
#     center = np.array([[center[0], center[0]]])
#     print "center"
#     print center
#     plt.scatter([center[0][0]], [center[0][1]], c=color, s=500, linewidths=5, marker="x")


# def data_exploration():
#     files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
#     colors = list(six.iteritems(matplot_colors.cnames))
#     data_idx_ranges = []  # start and end idxs for each column
#     prev_idx = -1
#     data = np.empty([0,1])
#     for idx, fname in enumerate(files):
#         col = pd.read_csv("data/"+fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname], dtype=np.float64)#.as_matrix()
#         print "col shape"
#         print col.shape
#         data_idx_ranges.append([prev_idx+1, prev_idx+1+col.shape[0]]) # store the start and end index of col in data
#         print "idx ranges: "
#         print data_idx_ranges[idx]
#         prev_idx += col.shape[0]
#         print "data shape now:"
#         print data.shape
#         data = np.append(data, col, axis=0)
#         print "data share after: "
#         print data.shape
#         #explore_single_column(col, colors[idx], marker="+")
#     print "final shape: "
#     print data.shape
#     for i in range(len(data_idx_ranges)):
#         explore_single_column(data[data_idx_ranges[i][0]: data_idx_ranges[i][1]], i, colors[i], marker="o")
#     plt.show()


def training():
    files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
    colors = list(six.iteritems(matplot_colors.cnames))
    data_idx_ranges = []  # start and end idxs for each column
    prev_idx = -1
    data = np.empty([0,2])
    for idx, fname in enumerate(files):
        col = pd.read_csv("data/"+fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=[fname], dtype=np.float64).as_matrix()
        col = np.append(col, col, 1)  # this to append col to col, so it will result in a matrix with two identical cols
        #print "col: "
        #print col
        data_idx_ranges.append([prev_idx+1, prev_idx+1+col.shape[0]]) # store the start and end index of col in data
        prev_idx += col.shape[0]
        data = np.append(data, col, axis=0)  # this to append the new col to the old col (append rows)
    centers = []
    for i in range(len(data_idx_ranges)):
        col = data[data_idx_ranges[i][0]:data_idx_ranges[i][1]]
        center = compute_centroid_single_cluster(col, i)
        print "computer centroid: "
        print center
        # the 2 lines below are just to adjust for the save of having a single feature and use it as x and y
        # center = center.flatten()
        # center = np.array([[center[0], center[0]],])
        centers.append(center)
        explore_single_cluster(data[data_idx_ranges[i][0]: data_idx_ranges[i][1]], center, colors[i])
    print "centers: "
    print centers
    # print "new centers: "
    # centers = np.array(centers)
    # print centers
    # np.array(centers).flatten().reshape((data.shape[0], 2))
    # print "new centers:"
    # print centers
    print "X: "
    print data
    # centers = np.array(centers)
    # print centers
    model = FCM(n_clusters=len(files))
    model.cluster_centers_ = centers  # np.array(centers)
    model.fit(data)
    return model


def learning(model):  # testing
    files = ["novHighC.csv", "surface.csv"]
    for fname in files:
        pass
    model = model.fit()


def main():
    model = training()
    # plt.show()

main()



