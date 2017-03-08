from learning import train, measure_representativeness, test
import learning

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt



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
    training_files = ["code_postal.csv", "entrada.csv", "mayHighC.csv"]
    model = train(training_files)
    repr = measure_representativeness(model, training_files)
    print "\nrepresentativeness of the training files is: \n"
    for i in xrange(len(repr)):
        print "%s: %f" % (training_files[i], repr[i])
    testing_files = ["novHighC.csv", "nodeid.csv"]
    # m = test(model, testing_files)
    data = learning.get_data_from_files(training_files)
    # model.fit(data)
    model.draw_membership_area_balanced(data, num_of_areas=10)
    # model.draw_membership(data, show=False)
    #
    legend_item = get_legend(training_files, "x" * len(training_files))
    legend_item += get_legend(training_files, "o" * len(training_files))
    plt.legend(legend_item, training_files+training_files, numpoints=1)
    plt.show()




if __name__ == "__main__":
    main()

