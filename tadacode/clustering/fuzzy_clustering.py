
import numpy as np
import matplotlib.pyplot as plt
import math
import random

from moviepy.editor import VideoClip, ImageSequenceClip
from moviepy.video.io.bindings import mplfig_to_npimage

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
        self.u = None  # The membership
        self.m = m  # the fuzziness, m=1 is hard not fuzzy. see the paper for more info

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
            sum2_vec = 0.0#np.zeros(num_of_features)
            # sum2_vec = np.full(num_of_features, 0.01)  # to avoid division by zero
            for i in xrange(num_of_points):
                # print "u %d %d: %f" % (i, c, self.u[i][c])
                # print "m: "+str(self.m)
                interm1 = (self.u[i][c] ** self.m)
                # print "interm1: "
                # print interm1
                interm2 = interm1 * X[i]
                # print "interm2: "
                # print interm2
                # print "sum1_vec: "
                # print sum1_vec
                sum1_vec += interm2
                sum2_vec += (self.u[i][c] ** self.m)
            # This loop is to replace zeros by another small value to avoid division by zero
            # for i in xrange(num_of_features):
            #     if sum2_vec[i] == 0:
            #         sum2_vec[i] = 0.000000000001
            if sum2_vec == 0:
                sum2_vec = 0.000001
            # print "cluster: %d" % c
            # print "sum1: "+str(sum1_vec)
            # print "sum2: "+str(sum2_vec)
            centers.append(sum1_vec/sum2_vec)
        #centers = np.array(centers)
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
        # print "distance: point %d and cluster %d is %f" % (datapoint_idx+1, cluster_idx+1, d1)
        sum1 = 0.0
        #print "==============\npoint %d and cluster %d: " % (datapoint_idx + 1, cluster_idx + 1)
        for c in self.cluster_centers_: # this is to compute the sigma
            #d2 = self.distance_squared(X[datapoint_idx], c)
            d2 = self.distance_squared(c, X[datapoint_idx])
            #print " %f  / %f  = (%f) ^ (%f) => %f" %(d1, d2, (d1/d2), (1.0/(self.m-1)) ,(d1/d2) ** (1.0/(self.m-1)))
            # print "single: %f" % ((d1/d2) ** (1.0/self.m-1))
            sum1 += (d1/d2) ** (1.0/(self.m-1))
        #print "datapoint %d, cluster %d, sum: %f" % (datapoint_idx+1, cluster_idx+1,sum1)
        return sum1 ** -1

    def update_membership(self, X):
        """
        update the membership matrix
        :param X: data points
        :return: nothing

        For performance, the distance can be computed once, before the loop instead of computing it every time
        """
        for i in xrange(X.shape[0]):
            for c in xrange(len(self.cluster_centers_)):
                self.u[i][c] = self.compute_membership_single(X, i, c)

    def fit(self, X):
        print "X: "
        print X
        self.init_membership(X.shape[0])
        #self.test_membership()
        print "============\nmembership is: "
        print self.u
        list_of_centers = []
        for i in xrange(10):
            print "compute cluster centers"
            centers = self.compute_cluster_centers(X)
            print centers
            if i==0:
                init_centers = centers
            list_of_centers.append(centers)
            self.update_membership(X)
            print "updated membership is: "
            print self.u
        #self.draw_both_centers(init_centers, self.cluster_centers_, X)
        self.draw_centers_animation(list_of_centers, init_centers, X)


    def draw_centers_animation(self, list_of_centers, init_centers, X):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        colors = ["red", "blue", "green", "pink", "yellow", "brown", "black"]
        plots = []
        fig, ax = plt.subplots(1, figsize=(4, 4), facecolor=(1, 1, 1))
        for center in list_of_centers:
            plt.scatter(X[:, 0], X[:, 1], marker="o", alpha=0.3)
            for clus in range(self.n_clusters):
                x, y = init_centers[clus]
                ax.scatter([x], [y], c=colors[clus], marker="x", s=360, linewidths=5)
            for clus in range(self.n_clusters):
                x, y = center[clus]
                ax.scatter([x], [y], c=colors[clus], marker="+", s=560, linewidths=5)
                # ax.scatter([x], [y], c=colors[clus + len(self.cluster_centers_) + 1], marker="+", s=560, linewidths=5)
                # ax.scatter([x], [y], marker="+", c=colors[len(self.cluster_centers_)+1], s=560, linewidths=5, alpha=0.7)
            plots.append(mplfig_to_npimage(fig))
            ax.clear()
        #plt.show()
        clip = ImageSequenceClip(plots, fps=1)
        clip.write_gif('test.gif', fps=1)


    def draw_both_centers(self, centers1, centers2, X):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        # for idx, x in enumerate(X):
        #     x0, x1 = x
        #     for clus in range(n_clusters):
        #         if model.labels_[idx] == clus:
        #             cc = colors[clus]
        #             plt.scatter([x0], [x1], c=cc)  # draw points
        # plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color="red")
        plt.scatter(X[:,0], X[:,1], marker="o", alpha=0.3)
        for clus in range(self.n_clusters):
            x, y = centers1[clus]
            plt.scatter([x], [y], c=colors[clus], marker="x", s=360, linewidths=5)  # draw x
        for clus in range(self.n_clusters):
            x, y = centers2[clus]
            plt.scatter([x], [y], c=colors[clus+len(self.cluster_centers_)], marker="+", s=560, alpha=0.7, linewidths=5)  # draw x
        plt.show()



    ### The below is from the initial k-means, just to be used as a reference




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