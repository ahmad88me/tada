"""
    Here I'm trying to implement k-means and Fuzzy C-means and then compare them
"""




import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

def animation_example():
    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i/10.0))  # update the data
        return line,


    # Init only required for blitting to give a clean slate.
    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                                  interval=25, blit=False)
    plt.show()

#animation_example()


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

    def label_data(self, X, centers):
        labels = np.zeros(X.shape[0], dtype=np.int32)
        distances = np.zeros(X.shape[0])
        for pid, p in enumerate(X):  # p for point
            min_dist = None
            for l, c in enumerate(centers):  # l for label and c for center
                dist = math.sqrt(math.fabs(np.dot(c, p)))
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

    def fit(self, X):
        centers = self._init_centroids(X, self.n_clusters)
        self.cluster_centers_ = centers
        best_inertia = None
        for i in range(100):
            labels, distances = self.label_data(X, self.cluster_centers_)
            centers = self.recompute_centroids(X, self.cluster_centers_, labels, distances)
            _, new_distances = self.label_data(X, centers)
            inertia = np.sum(new_distances)
            if best_inertia is not None:
                print "best_inertia: %f " % best_inertia
                print "inertia: %f " % inertia
            else:
                print "new"
            if best_inertia is None or inertia < best_inertia:
                best_inertia = inertia
                self.cluster_centers_ = centers
                self.labels_ = labels
                self.inertia_ = new_distances
                print "yes"

        self.draw(X=X, n_clusters=self.n_clusters, model=self)
        return self

    def draw(self, n_clusters, X, model):
        from matplotlib import colors as matplot_colors
        import six
        colors = list(six.iteritems(matplot_colors.cnames))
        print model.labels_
        # print kmeans.cluster_centers_
        # plt.scatter(X[:,0], X[:,1])

        for idx, x in enumerate(X):
            x0, x1 = x
            for clus in range(n_clusters):
                if model.labels_[idx] == clus:
                    cc = colors[clus]
                    plt.scatter([x0], [x1], c=cc)  # draw points

        # plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color="red")
        for clus in range(n_clusters):
            x, y = model.cluster_centers_[clus]
            plt.scatter([x], [y], c=colors[clus], marker="x", s=120)  # draw x
        plt.show()


# #def test_kmeans():
# #from clustering import KMeans
# from matplotlib import colors as matplot_colors
# import six
# colors = list(six.iteritems(matplot_colors.cnames))
#
# n_clusters = 2
# X = np.array([[1.0, 2.0], [1.0, 4.0], [1.0, 0.0], [4.0, 2.0], [4.0, 4.0], [4.0, 0.0]])
# kmeans = KMeans(n_clusters=n_clusters).fit(X)
# print kmeans.labels_
# #print kmeans.cluster_centers_
# #plt.scatter(X[:,0], X[:,1])
#
# for idx, x in enumerate(X):
#     x0, x1 = x
#     for clus in range(n_clusters):
#         if kmeans.labels_[idx] == clus:
#             cc = colors[clus]
#             plt.scatter([x0], [x1], c=cc) # draw points
#
#
# #plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], color="red")
# for clus in range(n_clusters):
#     x, y = kmeans.cluster_centers_[clus]
#     plt.scatter([x], [y], c=colors[clus], marker="x", s=120) # draw x
# plt.show()


from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
X = StandardScaler().fit_transform(X)
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print X
kmeans = KMeans(n_clusters=n_clusters_).fit(X)


# from sklearn import datasets
# iris = datasets.load_iris()
#X = iris.data[:, :2]  # we only take the first two features.
#kmeans = KMeans(n_clusters=3).fit(X)

# X = np.array([[1.0, 2.0], [1.0, 4.0], [1.0, 0.0], [4.0, 2.0], [4.0, 4.0], [4.0, 0.0]])
# kmeans = KMeans(n_clusters=2).fit(X)


## Something is wrong with the Kmeans algorithm, I need to check to fix it. Maybe assigning the center of clusters
## would help figure out the problem

