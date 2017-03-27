
import numpy as np


def merge_data_and_meta_naive(data1=None, meta_data1=None, data2=None, meta_data2=None):
    """
    Naive because it does not merge similar types in meta data
    :param data1:
    :param meta_data1:
    :param data2:
    :param meta_data2:
    :return: data, meta_data
    """
    if data1 is None:
        print "merge_data_and_meta> data1 should not be None"
        return None, None
    if meta_data1 is None:
        print "merge_data_and_meta> meta_data1 should not be None"
        return None, None
    if data2 is None:
        print "merge_data_and_meta> data2 should not be None"
        return None, None
    if meta_data2 is None:
        print "merge_data_and_meta> meta_data2 should not be None"
        return None, None
    if data1.shape[1] != data2.shape[1]:
        print "merge_data_and_meta> num of columns in data1 does not match num of columns in data2"
        print "merge_data_and_meta> data1 num of cols %d, data2 num of cols %d" % (data1.shape[1], data2.shape[1])
        return None, None
    data = np.append(data1, data2, axis=0)
    meta_data = meta_data1
    for md in meta_data2:
        md["from_index"] += data1.shape[0]
        md["to_index"] += data1.shape[0]
        meta_data.append(md)
    return data, meta_data
