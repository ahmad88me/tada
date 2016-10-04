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
    good_data = data[((data[feature] >= Q1 - step) & (data[feature] <= Q3 + step))]
    return good_data


def draw_as_points(data, color_idx=0):
    data = data.round()  # round the temp to the closest
    temp_freq = data[0].value_counts()
    print type(temp_freq)
    print temp_freq
    print temp_freq.axes
    plt.scatter(temp_freq.axes, temp_freq.values, c=colors[color_idx])
    plt.xlabel('Temperature', fontsize=16)
    plt.ylabel('Frequencies', fontsize=16)


def draw_features(features, color_idx=0, marker="o", s=20, alpha=0.5):
    # plt.scatter(features[0], features[1], c=colors[color_idx], marker=marker, s=s, alpha=alpha)
    #print "draw features color: %d" % (color_idx)
    #plt.scatter(features[0], features[1], c=color_idx, marker=marker, s=s, alpha=alpha, cmap=plt.cm.jet)
    colo = len(features) * [color_idx]
    #print "colo: "
    #print color_idx
    plt.scatter(features[0], features[1], s=s, marker=marker, alpha=alpha,  c=colors[color_idx])


def draw_features_cluster(data, num_of_clusters):
    #plt.scatter(data[0], data[1], c=y_pred, cmap=plt.cm.jet)
    for clus in range(num_of_clusters):
        clus_x = data[(data['pred']==clus)]
        print 'clus: %d' % clus
        print clus_x
        plt.scatter(clus_x[0], clus_x[1], c=colors[clus])


def compute_standard_deviation(data):
    return data.std()


def compute_mean(data):
    return data.mean()


def compute_media(data):
    return data.median()


def compute_features(data):
    return {0: compute_standard_deviation(data), 1: compute_mean(data)}


def start_processing(fname, color_idx=None, drop_out=False):
    data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False)
    num_before = data.count()
    print "number of rows before cleaning: %d" % num_before
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data.dropna(inplace=True)
    num_after = data.count()
    print "number of rows after the cleaning: %d" % num_after
    print "bad values: %d" % (num_before - num_after)
    print "mean: %f.2" % (data.mean())
    kfold = KFold(n_splits=5)
    features_list = []
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
            #draw_features(features.values(), c_idx, marker="^", s=200, alpha=0.5)
            draw_features(features.values(), color_idx, marker="^", s=200, alpha=0.5)
            features["label"] = color_idx
            df = pd.DataFrame(features)
            features_list.append(df)
        else:
            features = compute_features(train_data)
            features_list.append(features)
            #draw_features(features, c_idx, marker="o")

    return pd.concat(features_list)


def cluster(data, num_of_clusters):
    x=data[[0,1]]
    y=data['label']
    means = []
    for clus in range(num_of_clusters):
        clus_x = data[(data['label']==clus)]
        #print 'clus: %d' % clus
        #print clus_x
        means.append([clus_x[0].mean(), clus_x[1].mean()])
    # print 'x'
    # print x
    # print 'y'
    # print y
    # clusterer = KMeans(n_clusters=num_of_clusters)
    # clusterer = GaussianMixture(n_components=num_of_clusters, means_init=means)
    clusterer = GaussianMixture(n_components=num_of_clusters)
    clusterer.fit(x, y)
    print 'clusterer means: '
    print clusterer.means_
    for clus in range(num_of_clusters):
        xx, yy = clusterer.means_[clus]
        plt.scatter([xx], [yy], c=colors[clus], marker="s", s=200, alpha=0.5)
    means = np.array(means)
    print 'computer means:'
    print means
    #print pd.DataFrame(means)
    clusterer.means_ = means
    print 'clusterer new means: '
    print clusterer.means_
    for clus in range(num_of_clusters):
        xx, yy = clusterer.means_[clus]
        plt.scatter([xx], [yy], c=colors[clus], marker="d", s=200, alpha=0.5)
    preds = clusterer.predict(x)
    data['pred'] = preds
    draw_features_cluster(data, num_of_clusters)


def test(fname, color_idx=10):
    data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False)
    num_before = data.count()
    print "number of rows before cleaning: %d" % num_before
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data.dropna(inplace=True)
    num_after = data.count()
    #print "number of rows after the cleaning: %d" % num_after
    #print "bad values: %d" % (num_before - num_after)
    #print "mean: %f.2" % (data.mean())
    data = drop_outliers(data, 0)
    features = compute_features(data)
    draw_features(features, color_idx, marker="s", s=200)


def main():
    fnames = ["novHighC.csv",  "surface.csv", "code_postal.csv", "nodeid.csv", "entrada.csv"]
    features_list = []
    for idx, fname in enumerate(fnames):
        fl = start_processing(fname, idx, drop_out=True)
        features_list.append(fl)
    df = pd.concat(features_list)
    #print "df main"
    #print df
    cluster(df, len(fnames))
    # test("mayHighC.csv")
    plt.xlabel('Temperature')
    plt.ylabel('Standard Deviation')
    plt.show()
main()




