
import os
import pandas as pd
import numpy as np

import random
import matplotlib.pyplot as plt
import matplotlib.cm
from matplotlib.colors import rgb2hex
from matplotlib import colors as matplot_colors
import six
colors = list(six.iteritems(matplot_colors.cnames))
colors_hex = zip(*colors)[1]

#cmap = matplotlib.cm.get_cmap(name='viridis')
cmap = matplotlib.cm.get_cmap(name='hsv')
print "cmap N: "+str(cmap.N)

input_files = [
    "badmintonplayers.csv",
    "basketballplayers.csv",
    "boxers.csv",
    "cyclists.csv",
    "golfplayers3.csv",
    "gymnasts.csv",
    "handballplayers.csv",
#    "mountains.csv",
    "Olympic Games.csv",
    "rower.csv",
    "soccerplayers4.csv",
    "stadiums2.csv",
    "swimmers.csv",
    "tennisplayers.csv",
    "volleyballplayers.csv",
    "wrestlers.csv",
]

#d = "../../docs/kcap2017/"
d = "clean_input"
d = "/Users/aalobaid/workspaces/Pyworkspace/tada/tadacode/explore/clean_input"
#f = open(os.path.join(d, input_files[0]))
#print f.readline()


#df = pd.read_csv(os.path.join(d, input_files[1])).select_dtypes(include=[np.number]).dropna(axis=1, how='any')
#plt.scatter(df['Year'], df['Year'], c=colors[0], alpha=0.5)


# for idx, column in enumerate(df):
#     m = df[column].mean()
#     plt.plot(df[column], [m] * df[column].size, "o", c=colors_hex[idx], alpha=0.5, label=column)
#
# plt.legend()
#
# plt.show()


def get_outliers(df, k=1.5):
    q1 = df.quantile(q=0.25)
    q3 = df.quantile(q=0.75)
    return df[(df < q1 - k * (q3 - q1)) | (df > q3 + k * (q3 - q1))]


color_idx = 0
for idx_inp, inpf in enumerate(input_files):
    #print "inpf: "+inpf
    #print idx_inp
    df = pd.read_csv(os.path.join(d, inpf)).select_dtypes(include=[np.number]).dropna(axis=1, how='any')
    for idx, column in enumerate(df):
        if df[column].size == 0:
            continue
        # m = df[column].mean()
        # plt.plot(df[column], [m] * df[column].size, "o", c=colors_hex[color_idx], alpha=0.5, label=column[0:6]+"("+inpf[0:4]+")")
        # plt.plot(df[column], [m] * df[column].size, random.choice(["^","v","<",">","1","2","3","4","P","X"]), c=rgb2hex(cmap(color_idx%cmap.N)), alpha=0.5,
        #          label=column[0:6] + "(" + inpf[0:4] + ")")
        plt.plot(df[column], [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"] * df[column].size, "o",
                 c=rgb2hex(cmap(color_idx % cmap.N)), alpha=0.5, label=column[0:6] + "(" + inpf[0:4] + ")")
        color_idx += 15
        # q1 = df[column].quantile(q=0.25)
        # q3 = df[column].quantile(q=0.75)
        # k = 1.5
        # k2 = 2.0
        # outliers = df[column][(df[column] < q1 - k * (q3 - q1)) | (df[column] > q3 + k * (q3 - q1))]
        outliers = get_outliers(df[column])
        if outliers.size != 0:
        #if not df[column].between(q1 - k*(q3-q1), q3 + k*(q3-q1)).all():
            print column.lower() + "(" + inpf.lower() + ")"


#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()






