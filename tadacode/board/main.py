from learning import train_from_files, train_from_class_uris, measure_representativeness
import learning
import easysparql
from __init__ import META_ENDPOINT, RAW_ENDPOINT

import subprocess

import numpy as np

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
#import vispy.mpl_plot as plt

import matplotlib
print matplotlib.get_backend()

# The below two function are copied from http://stackoverflow.com/questions/5478351/python-time-measure-function
import functools, time


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc
#
# @timeit
# def foobar():
#     mike = Person()
#     mike.think(30)


def onclick(event):
    print 'event.ind'
    print event.ind
    ind = event.ind
    print 'onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind)
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))


def get_legend(names, markers):
    from matplotlib import colors as matplot_colors
    import six
    colors = list(six.iteritems(matplot_colors.cnames))
    c = []
    for idx, name in enumerate(names):
        c.append(Line2D([0], [0], color=colors[idx][1], marker=markers[idx], linestyle='None'))
    return c


#@timeit
def main():
    fig = plt.figure()
    #ax = fig.add_subplot(111)
    ax = fig.add_subplot(111)
    training_files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
    model = train_from_files(training_files)
    repr = measure_representativeness(model, training_files)
    print "\nrepresentativeness of the training files is: \n"
    for i in xrange(len(repr)):
        print "%s: %f" % (training_files[i], repr[i])
    testing_files = ["novHighC.csv", "nodeid.csv"]
    # m = test(model, testing_files)
    data = learning.get_data_from_files(training_files)
    model.fit(data)
    model.draw_membership_area_balanced_opengl(data, num_of_areas=20)
    #model.draw_membership_area_balanced(data, ax, num_of_areas=20)
    #model.draw_membership_area_balanced_vispy(data, num_of_areas=10)
    #ax = model.draw_membership(data, ax, show=False)
    legend_item = get_legend(training_files, "x" * len(training_files))
    legend_item += get_legend(training_files, "o" * len(training_files))
    plt.legend(legend_item, training_files+training_files, numpoints=1)
    print "preparing to show"

    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('pick_event', onclick)
    #plt.show()


def main_sparql():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    class_uri = 'http://schema.org/SportsTeam'
    model = train_from_class_uris(class_uris=[class_uri])
    # data = learning.get_data_from_uris(meta_endpoint=META_ENDPOINT, raw_endpoint=RAW_ENDPOINT, class_uris=[class_uri],
    #                                    property_min_count=50, top_k_properties_per_class=5)
    # testing_files = ["novHighC.csv", "nodeid.csv"]

    # m = test(model, testing_files)

    # data = learning.get_data_from_files(training_files)

    # model.fit(data)

    #model.draw_membership_area_balanced(data, ax, num_of_areas=20)
    #model.draw_membership_area_balanced_vispy(data, num_of_areas=10)

    # ax = model.draw_membership(data, ax, show=False)
    # legend_item = get_legend(training_files, "x" * len(training_files))
    # legend_item += get_legend(training_files, "o" * len(training_files))
    # plt.legend(legend_item, training_files+training_files, numpoints=1)
    # print "preparing to show"

    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    cid = fig.canvas.mpl_connect('pick_event', onclick)
    plt.show()


def main_manual_sparql():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    class_property_combinations = [
        ('http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/numberOfMatches'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longew'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latns'),
        ('http://schema.org/Place', 'http://www.georss.org/georss/point'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]
    # for class_uri, propert_uri in class_property_combinations:
    #     easysparql.get_objects_as_list(endpoint=RAW_ENDPOINT, class_uri=class_uri, property_uri=propert_uri)
    model, data, meta_data = learning.train_from_class_property_uris(class_property_uris=class_property_combinations,
                                                          get_data=True, get_meta_data=True)
    # testing_files = ["novHighC.csv", "nodeid.csv"]

    # m = test(model, testing_files)

    # data = learning.get_data_from_files(training_files)

    model.fit(data)
    # learning.inspect_membership(meta_data, model.u)
    learning.compute_representativeness_from_meta(meta_data, model.u)
    max_x, min_x, max_y, min_y = model.draw_membership_area_balanced_opengl(data, num_of_areas=100)
    #model.draw_membership_area_balanced(data, ax, num_of_areas=20)
    #model.draw_membership_area_balanced_vispy(data, num_of_areas=10)


    # ax = model.draw_membership(data, ax, show=False)
    # legend_item = get_legend(training_files, "x" * len(training_files))
    # legend_item += get_legend(training_files, "o" * len(training_files))
    # plt.legend(legend_item, training_files+training_files, numpoints=1)
    print "preparing to show"
    comm = "python board/scatter.py local_points.in '' %f %f %f %f %d %d %f" % (max_x, min_x, max_y, min_y, 600, 600,
                                                                                600/100.0)
    print comm
    subprocess.call(comm, shell=True)
    # subprocess.call("python board/scatter.py local_points.in %f %f %f %f %d %d %f"
    #                 % (max_x, min_x, max_y, min_y, 600, 600, 600/100.0), shell=True)


    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    #cid = fig.canvas.mpl_connect('pick_event', onclick)
    #plt.show()


if __name__ == "__main__":
    #main()
    #main_sparql()
    main_manual_sparql()


# import sys
# #sys.path.append('/Users/aalobaid/workspaces/Pyworkspace/tada/tadacode')
# sys.path.append('/Users/aalobaid/workspaces/Pyworkspace/tada/tadacode/board')
# from learning import train, measure_representativeness
# import learning
#
# import numpy as np
#
# from matplotlib.lines import Line2D
# import matplotlib.pyplot as plt
# #import vispy.mpl_plot as plt
#
# import matplotlib
# print matplotlib.get_backend()

from board.test import AnnoteFinder


# x = range(10)
# y = range(10)
# annotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
# fig, ax = plt.subplots()
# ax.scatter(x[:5],y[:5])
# ax.scatter(x[5:],y[5:])
# af = AnnoteFinder(x,y, annotes, ax=ax)
# fig.canvas.mpl_connect('button_press_event', af)
# plt.show()
#
#



# fig = plt.figure()
# ax = fig.add_subplot(111)
# fig, ax = plt.subplots()
# if ax is None:
#     print 'ax is none in main'
# training_files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
# model = train(training_files)
# repr = measure_representativeness(model, training_files)
# print "\nrepresentativeness of the training files is: \n"
# testing_files = ["novHighC.csv", "nodeid.csv"]
# # m = test(model, testing_files)
# data = learning.get_data_from_files(training_files)
# model.fit(data)
# #model.draw_membership_area_balanced(data, ax, num_of_areas=20)
# # model.draw_membership_area_balanced_vispy(data, num_of_areas=10)
# model.draw_membership(data, ax, show=False)
# print "preparing to show"
#
#
#
# x = data[:,0]
# y = data[:,1]
# # annotes =  model.u
# annotes = ['aslkdjf'] * data.shape[0]
# print 'len annotes'
# print len(annotes)
# af = AnnoteFinder(x,y, annotes, ax=ax)
# fig.canvas.mpl_connect('button_press_event', af)
# plt.show()
