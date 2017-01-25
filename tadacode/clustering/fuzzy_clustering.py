
import numpy as np
import matplotlib.pyplot as plt
import math
import random

from moviepy.editor import VideoClip, ImageSequenceClip
from moviepy.video.io.bindings import mplfig_to_npimage

import matplotlib
matplotlib.use("Agg")# the below line is needed for pygame to be used int moviepy preview


def compute_single_color(p, color):
    import textwrap
    if p >= 0.75:
        p = 1.0
    new_color = [0.0, 0.0, 0.0]
    for c in range(len(new_color)):
        new_color[c] += int("0x" + textwrap.wrap(color.replace("#", ""), 2)[c], 0) * p
        new_color[c] = int(new_color[c])
    return "#%02x%02x%02x" % (new_color[0], new_color[1], new_color[2])


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

    def __init__(self, n_clusters=2, m=2, max_iter=10):
        self.n_clusters = n_clusters
        self.cluster_centers_ = None
        self.u = None  # The membership
        self.m = m  # the fuzziness, m=1 is hard not fuzzy. see the paper for more info
        self.max_iter = max_iter

    def test_membership(self):
        # self.u = np.array([[ 0.9,  0.1],
        #                    [0.9, 0.1],
        #                    [ 0.5,  0.5],
        #                 [0.9, 0.1],
        #  [ 0.7,  0.3],
        #  [ 0.6,  0.4]])
        self.u = np.array([[0.9, 0.1], [0.9, 0.1], [0.2, 0.8], [0.2, 0.8]])

    def init_membership(self, num_of_points):
        self.init_membership_random(num_of_points)

    def init_membership_equal(self, num_of_points):
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

    def init_membership_random(self, num_of_points):
        """
        :param num_of_points:
        :return: nothing

        """
        self.u = np.zeros((num_of_points, self.n_clusters))
        for i in xrange(num_of_points):
            row_sum = 0.0
            for c in xrange(self.n_clusters):
                if c == self.n_clusters-1:  # last iteration
                    self.u[i][c] = 1.0 - row_sum
                else:
                    rand_clus = random.randint(0, self.n_clusters-1)
                    rand_num = random.random()
                    rand_num = round(rand_num, 2)
                    # rand_num = round(1.0/self.n_clusters, 2)
                    # print "rand_num: %f" % rand_num
                    if rand_num + row_sum <= 1.0:  # to prevent membership sum for a point to be larger than 1.0
                        self.u[i][rand_clus] = rand_num
                        row_sum += self.u[i][rand_clus]

    def compute_cluster_centers(self, X):
        """
        :param X:
        :return:

        vi = (sum of membership for cluster i ^ m  * x ) / sum of membership for cluster i ^ m  : for each cluster i

        """
        num_of_points = X.shape[0]
        num_of_features = X.shape[1]
        centers = []
        for c in xrange(self.n_clusters):
            sum1_vec = np.zeros(num_of_features)
            sum2_vec = 0.0
            for i in xrange(num_of_points):
                interm1 = (self.u[i][c] ** self.m)
                interm2 = interm1 * X[i]
                sum1_vec += interm2
                sum2_vec += (self.u[i][c] ** self.m)
            if sum2_vec == 0:
                sum2_vec = 0.000001
            centers.append(sum1_vec/sum2_vec)
        self.cluster_centers_ = centers
        return centers

    def distance_squared(self, x, c):
        """
        Compute the Euclidean distance
        :param x: is a single point from the original data X
        :param c: is a single point that represent a center or a cluster
        :return: the distance
        """
        sum_of_sq = 0.0
        # print "compute distance squared"
        # print "x: "
        # print x
        # print "c: "
        # print c
        # print "len x: "
        # print len(x)
        # print "x[0]: "
        # print x[0]
        # print "c[0]: "
        # print c[0]
        for i in xrange(len(x)):
            sum_of_sq += (x[i]-c[i]) ** 2
        # print "sum or sq: "
        # print sum_of_sq
        return sum_of_sq

    def compute_membership_single(self, X, datapoint_idx, cluster_idx):
        """
        :param datapoint_idx:
        :param cluster_idx:
        :return: return computer membership for the given ids
        """
        # print "compute membership single"
        # print "cluster centers: "
        # print self.cluster_centers_
        # print "cluster centers [%d]: " % cluster_idx
        # print self.cluster_centers_[cluster_idx]
        d1 = self.distance_squared(X[datapoint_idx], self.cluster_centers_[cluster_idx])
        # print "d1: "
        # print d1
        sum1 = 0.0
        for c in self.cluster_centers_:  # this is to compute the sigma
            d2 = self.distance_squared(c, X[datapoint_idx])
            sum1 += (d1/d2) ** (1.0/(self.m-1))
        # print "sum1: "
        # print sum1
        return sum1 ** -1

    def update_membership(self, X):
        """
        update the membership matrix
        :param X: data points
        :return: nothing

        For performance, the distance can be computed once, before the loop instead of computing it every time
        """
        # print "shape of u: %s" % str(self.u.shape)
        for i in xrange(X.shape[0]):
            for c in xrange(len(self.cluster_centers_)):
                # print "i: %d c: %d" % (i,c)
                self.u[i][c] = self.compute_membership_single(X, i, c)

    def fit(self, X):
        if self.cluster_centers_ is None:
            do_compute_cluster_centers = True
        else:
            do_compute_cluster_centers = False

        # print "X: "
        # print X
        self.init_membership(X.shape[0])
        # self.test_membership()
        # print "============\nmembership is: "
        # print self.u
        list_of_centers = []
        membership_history = []
        membership_history.append(self.u.copy())
        for i in xrange(self.max_iter):
            if do_compute_cluster_centers:
                centers = self.compute_cluster_centers(X)
                if i == 0:
                    init_centers = centers
                list_of_centers.append(centers)
            else:
                init_centers = self.cluster_centers_
                list_of_centers = [init_centers]
            self.update_membership(X)
            membership_history.append(self.u.copy())
            print "updated membership is: "
            print self.u
        # self.draw_animation(list_of_centers, init_centers, X, membership_history)
        self.draw_membership_area(X)

    def predict(self, X):
        # print "will copy the membership"
        u = self.u.copy()
        # print "will construct a new array for the prediction"
        self.u = np.zeros((X.shape[0], self.n_clusters))
        # print "will update the membership"
        self.update_membership(X)
        # print "will copy the predicted membership"
        predicted_u = self.u.copy()
        # print "will revert back to the old membership"
        self.u = u
        return predicted_u

    def draw_points(self, ax, X, colors, u, marker="o", lw=1):
        for idx, xx in enumerate(X):
            x, y = xx
            c = []
            # for clus, m in enumerate(self.u[idx]):
            #     c.append(compute_single_color(m, colors[clus]))
            # ax.scatter([x], [y], c=colors_mean(c), marker="o", alpha=1.0)
            for clus, m in enumerate(u[idx]):
                ax.scatter([x], [y], c=compute_single_color(m, colors[clus]), marker=marker, alpha=m, lw=lw)
        return ax

    def draw_animation(self, list_of_centers, init_centers, X, membership_history):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        colors = zip(*colors)[1]
        plots = []
        fig, ax = plt.subplots(1, figsize=(4, 4), facecolor=(1, 1, 1))
        for idx, center in enumerate(list_of_centers):
            ax = self.draw_points(ax, X, colors, membership_history[idx])
            # for clus in range(self.n_clusters):
            #     x, y = init_centers[clus]
            #     ax.scatter([x], [y], c=colors[clus], marker="x", s=360, linewidths=5)
            for clus in range(self.n_clusters):
                x, y = center[clus]
                ax.scatter([x], [y], c=colors[clus], marker="+", s=560, linewidths=5)

            plots.append(mplfig_to_npimage(fig))
            ax.clear()
        clip = ImageSequenceClip(plots, fps=2)
        clip.write_gif('test.gif', fps=2)
        clip.preview()

    def draw_membership_area(self, X):
        print "draw membership"
        reduced_data = X
        model = self
        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = 1000 #0.06 # .02  # point in the mesh [x_min, x_max]x[y_min, y_max].
        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
        y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        print "will predict now"
        # Obtain labels for each point in mesh. Use last trained model.
        ttt = np.c_[xx.ravel(), yy.ravel()]
        print ttt
        print ttt.shape
        u = model.predict(np.c_[xx.ravel(), yy.ravel()])
        print "predicted"
        plt.figure(1)
        plt.clf()
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        colors = zip(*colors)[1]
        print "xx: "
        print xx
        print "yy: "
        print yy

        # I will try to flatten xx, yy and Z to see what would happen
        xx = xx.flatten()
        yy = yy.flatten()
        # print "xx: flatten "
        # print xx
        # print "yy: flatten"
        # print yy
        ax = plt
        print "will draw points"
        # ax = self.draw_points(ax, X, colors, u)
        ax = self.draw_points(ax, zip(xx,yy), colors, u, marker="s", lw=0)
        ax = self.draw_points(ax, X, colors, self.u, marker="o")
        print "will draw centers"
        for clus in range(self.n_clusters):
            ax.scatter([self.cluster_centers_[clus][0]], [self.cluster_centers_[clus][1]], c=colors[clus], marker="x", s=560, linewidths=5)
        print "will show"
        # ax.show()
        plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
                  'Centroids are marked with white cross')
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        plt.xticks(())
        plt.yticks(())
        plt.show()
