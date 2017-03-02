import __init__

import numpy as np
import pandas as pd

from clustering.fuzzy_clustering import FCM

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
    return np.append(col, col, 1)


def get_centroids_for_files(files):
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


def measure_representativeness(model, files):
    """
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


def train(training_files):
    """
    This function is responsible for training the model and compute the representative of each file
    :return: FCM model
    """
    centroids = get_centroids_for_files(training_files)
    # print "centroids: "
    # print centroids
    # max_iter =1 because the centers are precomputed
    model = FCM(n_clusters=len(training_files), max_iter=1)
    model.cluster_centers_ = centroids
    return model


def main():
    training_files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
    model = train(training_files)
    repr = measure_representativeness(model, training_files)
    print "\nrepresentativeness of the training files is: \n"
    for i in xrange(len(repr)):
        print "%s: %f" % (training_files[i], repr[i])

if __name__ == "__main__":
    main()

