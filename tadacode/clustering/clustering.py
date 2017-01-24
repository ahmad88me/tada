"""
    Here I'm trying to implement k-means and Fuzzy C-means and then compare them
"""

import numpy as np
import matplotlib.pyplot as plt
import math


def colors_mean(colors):
    """
    :param colors: list of colors
    :return: average hex formatted color
    """
    import textwrap
    new_color = [0.0, 0.0, 0.0]
    for whole_color in colors:
        for c in range(len(new_color)):
            new_color[c] += int("0x"+textwrap.wrap(whole_color.replace("#", ""), 2)[c], 0) / len(colors)
    return "#%02x%02x%02x" % (new_color[0], new_color[1], new_color[2])

def compute_single_color(p, color):
    """
    :param p: probability
    :param color: a hex formatted color
    :return: computed color in hex
    """
    # print "compute single color"
    # print color
    if p<0.30:
        p = 0.0
    elif p<0.70:
        p = 0.50
    else:
        p = 1.0

    import textwrap
    new_color = [0.0, 0.0, 0.0]
    for c in range(len(new_color)):
        # print "[%d] = %d" % (c, int("0x"+textwrap.wrap(color.replace("#", ""), 2)[c], 0))
        new_color[c] += int("0x"+textwrap.wrap(color.replace("#", ""), 2)[c], 0) * p
        new_color[c] = int(new_color[c])
    #     print new_color[c]
    # print new_color
    return "#%02x%02x%02x" % (new_color[0], new_color[1], new_color[2])
    # return new_color

# This doesn't seem right, check the for loop below
def compute_color(membership, colors):
    """
    :param membership: a matrix of probabilities for belonging to each cluster
    :param colors: a list of hex formatted colors for each cluster (one color for each cluster)
    :return: computed color in hex
    """
    import textwrap
    new_color = [0.0, 0.0, 0.0]
    for i, p in enumerate(membership):
        for c in range(len(colors)):  # check this for loop
            # print "part: "+textwrap.wrap(colors[i].replace("#", ""),2)[c]
            new_color[c] += int("0x"+textwrap.wrap(colors[i].replace("#", ""), 2)[c], 0) * p
    # print new_color
    for c in range(len(colors)):
        new_color[c] = int(new_color[c]/len(membership))
    print new_color
    # return "#%.2d%.2d%.2d" % (new_color[0], new_color[1], new_color[2])
    return "#%02x%02x%02x" % (new_color[0], new_color[1], new_color[2])


class KMeans:
    """
        Implementation highly inspired by sklearn
    """
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None

    def _init_centroids(self, X, k):
        n_samples = X.shape[0]
        seeds = np.random.permutation(n_samples)[:k]
        centers = X[seeds]
        return centers

    def eucl_dist(self, p1, p2):
        dist = 0
        # print "eucl_dist:"
        # print "diff"
        # print "p1"
        # print p1
        # print "p2"
        # print p2
        for i in range(len(p1)):
            dist += (p1[i] - p2[i]) ** 2
        # print "dist: "
        # print dist
        # print math.sqrt(dist)
        return math.sqrt(dist)

    def label_data(self, X, centers):
        labels = np.zeros(X.shape[0], dtype=np.int32)
        distances = np.zeros(X.shape[0])
        for pid, p in enumerate(X):  # p for point
            min_dist = None
            for l, c in enumerate(centers):  # l for label and c for center
                # dist = math.sqrt(math.fabs(np.dot(c, p)))
                dist = self.eucl_dist(c, p)
                # print "distance %f between %s and %s" % (dist, str(c), str(p))
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

    # Without updating the centroid
    # def fit(self, X):
    #     #centers = self._init_centroids(X, self.n_clusters)
    #     centers = np.array([[-1.5, -1], [1, -1], [1, 2]])
    #     self.cluster_centers_ = centers
    #     best_inertia = None
    #     for i in range(1):
    #         labels, distances = self.label_data(X, self.cluster_centers_)
    #         #centers = self.recompute_centroids(X, self.cluster_centers_, labels, distances)
    #         _, new_distances = self.label_data(X, centers)
    #         inertia = np.sum(new_distances)
    #         if best_inertia is not None:
    #             print "best_inertia: %f " % best_inertia
    #             print "inertia: %f " % inertia
    #         else:
    #             print "new"
    #         if best_inertia is None or inertia < best_inertia:
    #             best_inertia = inertia
    #             self.cluster_centers_ = centers
    #             self.labels_ = labels
    #             self.inertia_ = new_distances
    #             print "yes"
    #
    #     self.draw(X=X, n_clusters=self.n_clusters, model=self)
    #     return self

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

    # Original
    def fit(self, X):
        centers = self._init_centroids(X, self.n_clusters)
        self.cluster_centers_ = centers
        best_inertia = None
        for i in range(100):
            labels, distances = self.label_data(X, self.cluster_centers_)
            centers = self.recompute_centroids(X, self.cluster_centers_, labels, distances)
            _, new_distances = self.label_data(X, centers)
            inertia = np.sum(new_distances)
            # if best_inertia is not None:
            #     print "best_inertia: %f " % best_inertia
            #     print "inertia: %f " % inertia
            # else:
            #     print "new"
            if best_inertia is None or inertia < best_inertia:
                best_inertia = inertia
                self.cluster_centers_ = centers
                self.labels_ = labels
                self.inertia_ = new_distances
                print "yes"

        print "membership: "
        print self.get_memberships()
        # self.draw(X=X, n_clusters=self.n_clusters, model=self)
        # self.draw_with_areas(X, model=self)
        return self

    def draw(self, n_clusters, X, model):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        print "labels: "
        print model.labels_
        # print kmeans.cluster_centers_
        # plt.scatter(X[:,0], X[:,1])
        # colors = ["red", "blue", "green", "pink"]
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
        #colors = ["#FF0000", "#00FF00", "#0000FF"]
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



