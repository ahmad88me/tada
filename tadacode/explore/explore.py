
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


input_files = [
    "badmintonplayers.csv",
    "basketballplayers.csv",
    "boxers.csv",
    "cyclists.csv",
    "golfplayers3.csv",
    "gymnasts.csv",
    "handballplayers.csv",
    "Olympic Games.csv",
    "rower.csv",
    "soccerplayers4.csv",
    "stadiums2.csv",
    "swimmers.csv",
    "tennisplayers.csv",
    "volleyballplayers.csv",
    "wrestlers.csv",
]

d = "clean_input"


def get_outliers(df, k=1.5):
    q1 = df.quantile(q=0.25)
    q3 = df.quantile(q=0.75)
    return df[(df < q1 - k * (q3 - q1)) | (df > q3 + k * (q3 - q1))], df[(df >= q1 - k * (q3 - q1)) & (df <= q3 + k * (q3 - q1))]


def explore_input_files():
    color_idx = 0
    print "outliers in: "
    for idx_inp, inpf in enumerate(input_files):
        df = pd.read_csv(os.path.join(d, inpf)).select_dtypes(include=[np.number]).dropna(axis=1, how='any')
        for idx, column in enumerate(df):
            if df[column].size == 0:
                continue
            plt.plot(df[column], [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"] * df[column].size, ".",
                     c=rgb2hex(cmap(color_idx % cmap.N)), alpha=0.5, label=column[0:6] + "(" + inpf[0:4] + ")")
            outliers, _ = get_outliers(df[column])
            if outliers.size != 0:
                print " >  "+column.lower() + "(" + inpf.lower() + ")" + " num of outliers is: "+str(outliers.size)
                plt.plot(outliers, [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"] * outliers.size, "X",
                         c=rgb2hex(cmap(color_idx % cmap.N)), alpha=1.0, label=column[0:6] + "(" + inpf[0:4] + ")")
            color_idx += 15


def free_form_visualization():
    color_idx = 0
    for idx_inp, inpf in enumerate(input_files):
        df = pd.read_csv(os.path.join(d, inpf)).select_dtypes(include=[np.number]).dropna(axis=1, how='any')
        for idx, column in enumerate(df):
            if df[column].size == 0:
                continue
            plt.plot(df[column], [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"] * df[column].size, "1",
                     c=rgb2hex(cmap(color_idx % cmap.N)), alpha=0.3, label=column[0:6] + "(" + inpf[0:4] + ")")

            # draw the mean
            plt.plot([df[column].mean()], [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"], "s",
                     c=rgb2hex(cmap(color_idx % cmap.N)), alpha=0.5, label=column[0:6] + "(" + inpf[0:4] + ")")

            outliers, non_outliers = get_outliers(df[column])

            # draw the mean without the outliers
            plt.plot([non_outliers.mean()], [column[0:6].lower() + "(" + inpf[0:6].lower() + ")"], "D",
                     c=rgb2hex(cmap(color_idx % cmap.N)), alpha=0.5, label=column[0:6] + "(" + inpf[0:4] + ")")


            color_idx += 15
    line_up, = plt.plot([], [], "s", label='mean with outliers', c=rgb2hex(cmap(15 % cmap.N)))
    line_down, = plt.plot([], [], "D", label='mean without outliers', c=rgb2hex(cmap(15*10 % cmap.N)))
    plt.legend(handles=[line_up, line_down])

if raw_input("Enter:\n1) Data Exploration\n2) Free Form Visualization\n")=="1":
    explore_input_files()
else:
    free_form_visualization()
plt.show()






