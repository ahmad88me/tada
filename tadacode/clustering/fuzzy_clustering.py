
import numpy as np
import matplotlib.pyplot as plt
import math
import random

class FCM:
    """
        This algorithm is from the paper
        "FCM: The fuzzy c-means clustering algorithm" by James Bezdek
        Here we will use the Euclidean distance

        Pseudo code:
        1) Fix c, m, A
        c: n_clusters
        m: 2 by default
        A: we are using Euclidean distance, so we don't need it actually
        2) compute the means (cluster centers)
        3) update the membership matrix
        4) compare the new membership with the old one, is difference is less than a threshold, stop. otherwise
            return to step 2)
    """

    def __init__(self, n_clusters=2, m=2):
        self.n_clusters = n_clusters
        self.cluster_centers_ = None
        self.u = None # The membership
        self.m = m # the fuzziness, m=1 is hard not fuzzy. see the paper for more info

    def test_membership(self):
        self.u = np.array([[ 0.9,  0.1],
                           [0.9, 0.1],
                            [ 0.5,  0.5],
                          [0.9, 0.1],
         [ 0.7,  0.3],
         [ 0.6,  0.4]])

    def init_membership(self, num_of_points):
        """

        :param num_of_points:
        :return: nothing

        # In the below for loop, due to the rounding to 2 decimals, you may think that the membership sum for
        #  a point can be larger than 1. this can happen if number of clusters is larger than 10.
        # mathematical proof that this can happen:
        # (1) --- max_error per point membership to a single cluster is 0.01 (because of the rounding to 2 decimal
        #   points).
        # (2) --- (c-1) * 0.01 >= 1/c
        # (3) --- c^2 - c >= 1
        # solving for c we get c = 10.51 (approx.)
        # so when c >= 11, this error may occur.

        But I added a check below to prevent such a thing from happening
        """
        self.u = np.zeros((num_of_points, self.n_clusters))
        for i in xrange(num_of_points):
            row_sum = 0.0
            for c in xrange(self.n_clusters):
                if c == self.n_clusters-1:  # last iteration
                    self.u[i][c] = 1 - row_sum
                else:
                    rand_num = round(1.0/self.n_clusters, 2)
                    # print "rand_num: "
                    # print rand_num
                    if rand_num + row_sum >= 1.0:  # to prevent membership sum for a point to be larger than 1.0
                        if rand_num + row_sum - 0.01 >= 1.0:
                            print "ERROR: SOMETHING IS NOT RIGHT IN init_membership"
                            return None
                        else:
                            self.u[i][c] = rand_num - 0.01
                    else:
                        self.u[i][c] = rand_num
                    row_sum += self.u[i][c]

    # just copied from teh init_membership
    def init_membership_random(self, num_of_points):
        """
        just copied, it is not implemented yet.
        :param num_of_points:
        :return: nothing

        """
        self.u = np.zeros((num_of_points, self.n_clusters))
        for i in xrange(num_of_points):
            row_sum = 0.0
            for c in xrange(self.n_clusters):
                if c == self.n_clusters-1:  # last iteration
                    self.u[i][c] = 1 - row_sum
                else:
                    rand_num = round(1.0/self.n_clusters, 2)
                    # print "rand_num: "
                    # print rand_num
                    if rand_num + row_sum >= 1.0:  # to prevent membership sum for a point to be larger than 1.0
                        if rand_num + row_sum - 0.01 >= 1.0:
                            print "ERROR: SOMETHING IS NOT RIGHT IN init_membership"
                            return None
                        else:
                            self.u[i][c] = rand_num - 0.01
                    else:
                        self.u[i][c] = rand_num
                    row_sum += self.u[i][c]

    def compute_cluster_centers(self, X):
        """

        :param X:
        :return:

        vi = (sum of membership for cluster i ^ m  * x ) / sum of membership for cluster i ^ m  : for each cluster i

        """
        num_of_features = X.shape[1]
        centers = []
        for c in xrange(self.n_clusters):
            sum1_vec = np.zeros(num_of_features)
            sum2_vec = np.zeros(num_of_features)
            for i in xrange(num_of_features):
                interm1 = (self.u[i][c] ** self.m)
                # print "interm1: "
                # print interm1
                interm2 = interm1 * X[i]
                # print "interm2: "
                # print interm2
                # print "sum1_vec: "
                # print sum1_vec
                sum1_vec = sum1_vec + interm2
                sum2_vec += (self.u[i][c] ** self.m)
            centers.append(sum1_vec/sum2_vec)
        centers = np.array(centers)
        self.cluster_centers_ = centers
        return centers

    def distance_squared(self, x, c):
        """
        Computer the Euclidean distance
        :param x: is a single point from the original data X
        :param c: is a single point that represent a center or a cluster
        :return: the distance
        """
        sum_of_sq = 0.0
        for i in xrange(len(x)):
            sum_of_sq += (x[i]-c[i]) ** 2
        return sum_of_sq
        # return math.sqrt(sum_of_sq)

    def compute_membership_single(self, X, datapoint_idx, cluster_idx):
        """
        :param datapoint_idx:
        :param cluster_idx:
        :return: return computer membership for the given ids
        """
        d1 = self.distance_squared(X[datapoint_idx], self.cluster_centers_[cluster_idx])
        sum1 = 0.0
        for c in self.cluster_centers_:
            d2 = self.distance_squared(X[datapoint_idx], c)
            sum1 += (d1/d2) ** (1.0/self.m-1)
        return 1.0/sum1

    def update_membership(self, X):
        """
        update the membership matrix
        :param X: data points
        :return: nothing
        """
        for i in xrange(X.shape[0]):
            for c in xrange(len(self.cluster_centers_)):
                self.u[i][c] = self.compute_membership_single(X, i, c)

    def fit(self, X):
        print "X: "
        print X
        self.init_membership(X.shape[0])
        self.test_membership()
        print "membership is: "
        print self.u
        print "compute cluster centers"
        print self.compute_cluster_centers(X)
        self.update_membership(X)
        print "updated membership is: "
        print self.u


    ### The below is from the initial k-means, just to be used as a reference

    # def __init__(self, n_clusters=2):
    #     self.n_clusters = n_clusters
    #     self.cluster_centers_ = None
    #     self.labels_ = None
    #     self.inertia_ = None

    def _init_centroids(self, X, k):
        n_samples = X.shape[0]
        seeds = np.random.permutation(n_samples)[:k]
        centers = X[seeds]
        return centers

    def eucl_dist(self, p1, p2):
        dist = 0
        for i in range(len(p1)):
            dist += (p1[i] - p2[i]) ** 2
        return math.sqrt(dist)

    def label_data(self, X, centers):
        labels = np.zeros(X.shape[0], dtype=np.int32)
        distances = np.zeros(X.shape[0])
        for pid, p in enumerate(X):  # p for point
            min_dist = None
            for l, c in enumerate(centers):  # l for label and c for center
                dist = self.eucl_dist(c, p)
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    labels[pid] = l
                    distances[pid] = min_dist
        return labels, distances

    def recompute_centroids(self, X, centers, labels, distances):
        n_samples = X.shape[0]
        n_features = X.shape[1]
        n_clusters = centers.shape[0]
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

    def predict(self, X):
        labels, _ = self.label_data(X, self.cluster_centers_)
        return labels

    def get_memberships(self, labels=None):
        n_clusters = self.n_clusters
        if labels is None:
            llabels = self.labels_
        else:
            llabels = labels
        membership = np.zeros((llabels.shape[0], n_clusters))
        for i, l in enumerate(llabels):
            membership[i][l] = 1.0
        return membership

    # def fit(self, X):
    #     centers = self._init_centroids(X, self.n_clusters)
    #     self.cluster_centers_ = centers
    #     best_inertia = None
    #     for i in range(100):
    #         labels, distances = self.label_data(X, self.cluster_centers_)
    #         centers = self.recompute_centroids(X, self.cluster_centers_, labels, distances)
    #         _, new_distances = self.label_data(X, centers)
    #         inertia = np.sum(new_distances)
    #         if best_inertia is None or inertia < best_inertia:
    #             best_inertia = inertia
    #             self.cluster_centers_ = centers
    #             self.labels_ = labels
    #             self.inertia_ = new_distances
    #             print "yes"
    #
    #     print "membership: "
    #     print self.get_memberships()
    #     return self

    def draw(self, n_clusters, X, model):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        print "labels: "
        print model.labels_
        for idx, x in enumerate(X):
            x0, x1 = x
            for clus in range(n_clusters):
                if model.labels_[idx] == clus:
                    cc = colors[clus]
                    plt.scatter([x0], [x1], c=cc)  # draw points

        # plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color="red")
        for clus in range(n_clusters):
            x, y = model.cluster_centers_[clus]
            plt.scatter([x], [y], c=colors[clus], marker="x", s=360, linewidths=5)  # draw x
        plt.show()

    def draw_with_areas(self, X, model):
        reduced_data = X
        kmeans = model
        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .02  # point in the mesh [x_min, x_max]x[y_min, y_max].

        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last trained model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        # print Z
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        # print "Z: "
        # print Z[0]
        plt.figure(1)
        plt.clf()
        plt.imshow(Z,
                   interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   #cmap=plt.cm.Paired,
                   #cmap=plt.cm.Pastel1,
                   #cmap=plt.get_cmap('jet'),
                   #cmap=plt.cm.cool,
                   cmap=plt.cm.winter,
                   #cmap=plt.cm.Set1,
                   #cmap=plt.cm.Set3,
                   aspect='auto', origin='lower'
                   )

        plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'ko', markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)
        plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
                  'Centroids are marked with white cross')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.show()

    def draw_membership_area(self, X, model):
        reduced_data = X
        kmeans = model
        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = 0.07#.02  # point in the mesh [x_min, x_max]x[y_min, y_max].
        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last trained model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
        print "Z[0]: "
        print Z[0]
        print "\n\nZ: "
        print Z
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        print "Z: reshaped"
        print Z
        plt.figure(1)
        plt.clf()
        # plt.imshow(Z,
        #            interpolation='nearest',
        #            extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        #            # cmap=plt.cm.Paired,
        #            # cmap=plt.cm.Pastel1,
        #            # cmap=plt.get_cmap('jet'),
        #            # cmap=plt.cm.cool,
        #            # cmap=plt.cm.winter,
        #            # cmap=plt.cm.Set1,
        #            # cmap=plt.cm.Set3,
        #            aspect='auto', origin='lower'
        #            )
        # plt.scatter(xx, yy, c=Z, marker="s", lw = 0)
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        colors = zip(*colors)[1]
        colors = ["#FF0000", "#00FF00", "#0000FF"]
        new_Z = []
        print "xx: "
        print xx
        print "yy: "
        print yy

        # I will try to flatten xx, yy and Z to see what would happen
        xx = xx.flatten()
        yy = yy.flatten()
        Z = Z.flatten()

        print "xx: flatten "
        print xx
        print "yy: flatten"
        print yy

        # Commented the below for testing purposes
        for xy_idx in xrange(xx.shape[0]):
            x = xx[xy_idx]
            y = yy[xy_idx]
            # print "x: "
            # print x
            # print "y: "
            # print y
            # print "zip: "
            # print zip(xx,yy)
            colors_for_single_cluster = []
            for clusid, clus_center in enumerate(self.cluster_centers_):
                # print "clus_center: "
                # print clus_center
                dist = self.eucl_dist([x, y], clus_center)
                p = self.compute_prop_from_dist(dist, x_min, x_max, y_min, y_max)
                colors_for_single_cluster.append(compute_single_color(p, colors[clusid]))
            new_Z.append(colors_mean(colors_for_single_cluster))

        plt.scatter(xx, yy, c=new_Z, marker="s", lw=0)
        plt.scatter(xx, yy, c=Z, marker=".", lw=0, alpha=0.1)
        plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'ko', markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1],
                    marker='x', s=169, linewidths=3,
                    color='w', zorder=10)
        plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
                  'Centroids are marked with white cross')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.show()

    def compute_prop_from_dist(self, dist, x_min, x_max, y_min, y_max):
        x_diff = x_max - x_min
        y_diff = y_max - y_min
        x_diff /=3
        y_diff /=3
        if (x_diff) < (y_diff):
            return dist / x_diff
        else:
            return dist / y_diff