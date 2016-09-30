import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
# import data_exploration as dexplore


from matplotlib import colors as matplot_colors
import six

colors = list(six.iteritems(matplot_colors.cnames))


def drop_outliers(data, feature):
    Q1 = np.percentile(data[feature], 25)
    Q3 = np.percentile(data[feature], 75)
    step = (Q3 - Q1) * 1.5
    # data_outliers = data[~((data[feature] >= Q1 - step) & (data[feature] <= Q3 + step))]
    # outliers = data_outliers.index.values.tolist()
    # good_data = data.drop(data.index[outliers]).reset_index(drop = True)
    good_data = data[((data[feature] >= Q1 - step) & (data[feature] <= Q3 + step))]
    return good_data  # , data_outliers


def draw_as_points(data, color_idx=0):
    data = data.round() # round the temp to the closest
    #print data
    #data = data.apply(pd.value_counts)
    #temp_freq = data['temp'].value_counts()
    temp_freq = data[0].value_counts()
    print type(temp_freq)
    #print data
    #print data.iloc[:,0]
    #data['freq'] = freqv
    print temp_freq
    print temp_freq.axes
    plt.scatter(temp_freq.axes, temp_freq.values, c=colors[color_idx])
    plt.xlabel('Temperature', fontsize=16)
    plt.ylabel('Frequencies', fontsize=16)
    #data.iloc(0).value_counts()
    #plt.scatter(data.iloc(0)[:], [1 for _ in xrange(data.count())])
    #plt.show()


def draw_features(features, color_idx=0, marker="o", s=20, alpha=0.5):
    plt.scatter(features[0], features[1], c=colors[color_idx], marker=marker, s=s, alpha=alpha)

def draw_features_cluster(data, y_pred):
    plt.scatter(data[0], data[1], c=y_pred)


def compute_standard_deviation(data):
    return data.std()


def compute_mean(data):
    return data.mean()


def compute_media(data):
    return data.median()


def compute_features(data):
    return compute_standard_deviation(data), compute_mean(data)#, compute_media(data)

# def draw_mesh(reduced_data, num_of_clus):
#     kmeans = KMeans(init='k-means++', n_clusters=num_of_clus, n_init=10)
#     kmeans.fit(reduced_data)
#     # Step size of the mesh. Decrease to increase the quality of the VQ.
#     h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].
#
#     # Plot the decision boundary. For that, we will assign a color to each
#     x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
#     y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#
#     # Obtain labels for each point in mesh. Use last trained model.
#     Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
#
#     # Put the result into a color plot
#     Z = Z.reshape(xx.shape)
#     plt.figure(1)
#     plt.clf()
#     plt.imshow(Z, interpolation='nearest',
#                extent=(xx.min(), xx.max(), yy.min(), yy.max()),
#                cmap=plt.cm.Paired,
#                aspect='auto', origin='lower')
#
#     plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
#     # Plot the centroids as a white X


def start_processing(fname, color_idx=None, drop_out=False):
    #data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=['temp'])
    data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False)
    num_before = data.count()
    print "number of rows before cleaning: %d" % num_before
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data.dropna(inplace=True)
    num_after = data.count()
    print "number of rows after the cleaning: %d" % num_after
    print "bad values: %d" % (num_before - num_after)
    print "mean: %f.2" % (data.mean())
    #shuffle_split = ShuffleSplit(n_splits=5, train_size=0.2)
    #draw_as_points(data, 0)
    kfold = KFold(n_splits=5)
    features_list = []
    #features_list = pd.DataFrame()
    c_idx = 0
    for idx, (train, test) in enumerate(kfold.split(data)):
        train_data = data.iloc[train]
        if color_idx is None:
            c_idx = idx
        else:
            c_idx = color_idx
        if c_idx==4:
            c_idx+=1
        #draw_as_points(train_data, c_idx)
        if drop_out:
            train_data = drop_outliers(train_data, 0)
            features = compute_features(train_data)
            #df = pd.DataFrame(list(features))
            df = pd.DataFrame(features)
            print "features df"
            print df
            #features_list.append(features)
            features_list.append(df)
            #draw_features(features, c_idx, marker="o")
        else:
            features = compute_features(train_data)
            features_list.append(features)
            draw_features(features, c_idx, marker="o")

    #print "features_list: "
    #print features_list
    return pd.concat(features_list)
    #return features_list
    # fsegma, fmean = zip(*features_list)
    # if drop_out:
    #     draw_features([np.mean(fsegma), np.mean(fmean)], c_idx, marker="s", s=200)
    # else:
    #     draw_features([np.mean(fsegma), np.mean(fmean)], c_idx, marker="v", s=200)


def cluster(data, num_of_clusters):
    clusterer = KMeans(n_clusters=num_of_clusters)
    clusterer.fit(data)
    preds = clusterer.predict(data)
    print data
    draw_features_cluster(data, preds)


def test(fname, color_idx=10):
    data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False)
    num_before = data.count()
    print "number of rows before cleaning: %d" % num_before
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data.dropna(inplace=True)
    num_after = data.count()
    print "number of rows after the cleaning: %d" % num_after
    print "bad values: %d" % (num_before - num_after)
    print "mean: %f.2" % (data.mean())
    data = drop_outliers(data, 0)
    features = compute_features(data)
    draw_features(features, color_idx, marker="s", s=200)


def main():
    fnames = ["novHighC.csv",  "surface.csv", "code_postal.csv", "nodeid.csv", "entrada.csv"]
    # fnames = ["novHighC.csv", "surface.csv"]
    # fname = fnames[0]
    # start_processing(fname, None)
    features_list = []
    for idx, fname in enumerate(fnames):
        #start_processing(fname, idx)
        fl = start_processing(fname, idx, drop_out=True)
        print "fl: "
        print fl
        features_list.append(fl)
        #start_processing(fname, 2)
        #features_list.append(start_processing(fname, 1))
    df = pd.concat(features_list)
    cluster(df, len(fnames))
    #print "features list: "
    #print features_list[0][0]
    #draw_mesh(pd.DataFrame(features_list[0]), len(fnames))
    test("mayHighC.csv")
    plt.xlabel('Temperature')
    plt.ylabel('Standard Deviation')
    plt.show()
main()




