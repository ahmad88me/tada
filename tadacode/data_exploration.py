import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors as matplot_colors
import six
import math

colors = list(six.iteritems(matplot_colors.cnames))


def draw_as_catogories(data, color_idx):
    all_color_palette = ["Reds", "Blues"]
    color_palette = all_color_palette[color_idx%len(all_color_palette)]
    #print "min type"
    #print type(data['temp'].min())
    range_len = 1
    min_num = data['temp'].min()
    max_num = data['temp'].max()
    print "min: %f " % min_num
    print "max: %f" % max_num
    # min_num = int(min_num)
    # max_num = int(max_num)
    if min_num < 0:
        start_point = (min_num//range_len * range_len) #- range_len
        #print min_num//range_len
        #print (min_num//range_len * range_len)
        print "neg min %f" % start_point
    else:
        start_point = min_num//range_len * range_len
        print "pos min %f" % start_point
    if max_num < 0:
        end_point = (max_num//range_len * range_len) + range_len
        print "neg max %f" % end_point
    else:
        end_point = (max_num//range_len * range_len) + range_len
        print "pos max %f" % end_point

    #temp_as_cat = pd.cut(data['temp'], bins=range_len).value_counts()
    print range(int(start_point), int(end_point+1), int(range_len))
    temp_as_cat = pd.cut(data['temp'], bins=range(int(start_point), int(end_point+1), int(range_len))).value_counts()
    df = pd.DataFrame(temp_as_cat)
    df["intervals"] = df.index.values
    df.rename_axis({0: "freq"}, axis="columns", inplace=True)
    print df
    sns.set_style("whitegrid")
    #ax = sns.barplot(x="intervals", y="freq", data=df)
    ax = sns.barplot(x="intervals", y="freq", data=df, palette=sns.color_palette(color_palette, n_colors=7), alpha=0.5)
    ax.set(xlabel='Intervals', ylabel='Frequency')
    #sns.plt.show()


def draw_as_points(data, color_idx=0):
    data = data.round() # round the temp to the closest
    #print data
    #data = data.apply(pd.value_counts)
    temp_freq = data['temp'].value_counts()
    print type(temp_freq)
    #print data
    #print data.iloc[:,0]
    #data['freq'] = freqv
    print temp_freq
    print temp_freq.axes
    fff = []
    for i in temp_freq.values:
        fff.append(math.log(i))
    plt.scatter(fff, temp_freq.values, c=colors[color_idx])
    #plt.scatter(temp_freq.axes, temp_freq.values, c=colors[color_idx])
    plt.xlabel('Temperature', fontsize=16)
    plt.ylabel('Frequencies', fontsize=16)
    #data.iloc(0).value_counts()
    #plt.scatter(data.iloc(0)[:], [1 for _ in xrange(data.count())])
    plt.show()


def explore(fname, color_idx=1):
    data = pd.read_csv(fname, header=None, error_bad_lines=False, warn_bad_lines=False, names=['temp'])  # dtype=np.float64
    num_before = data.count()
    print "number of rows before cleaning: %d" % num_before
    # print data.iloc(0)[581] # invalid input
    data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data.dropna(inplace=True)
    # print data.iloc(0)[581] # invalid input is no longer there
    num_after = data.count()
    print "number of rows after the cleaning: %d" % num_after
    print "bad values: %d" % (num_before - num_after)
    print "mean: %.2f" % (data.mean())
    print "median: %.2f" % (data.median())
    print "standard deviation: %.2f" % (data.std())
    #draw(data)
    #return data
    draw_as_catogories(data, color_idx)

    #draw_as_points(data)

explore("CountrynovHighC.csv", 1)
explore("novHighC.csv", 0)

sns.plt.show()