from functools import partial
import numpy as np
import pandas as pd
import traceback

import easysparql
import data_extraction
import learning

from models import MLModel, PredictionRun, Membership


def get_classes(endpoint=None):
    if endpoint is None:
        print "get_classes> endpoint should not be None"
        return []
    return easysparql.get_classes(endpoint=endpoint)


def explore_and_train_tbox(endpoint=None, model_id=None):
    if endpoint is None:
        print "explore_and_train_tbox> endpoint is None"
        return
    if model_id is None:
        print "explore_and_train_tbox> model_id should not be None"
        return
    try:
        update_progress_func = partial(update_model_progress_for_partial, model_id)
        update_model_state(model_id=model_id, new_state=MLModel.RUNNING, new_progress=0,
                           new_notes="Extracting numerical class/property combinations")
        # Safe function
        classes_properties_uris = easysparql.get_all_classes_properties_numerical(endpoint=endpoint)
        update_model_state(model_id=model_id, new_progress=0,
                           new_notes="extracting values from gathered class/property")
        data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
            endpoint=endpoint, class_property_uris=classes_properties_uris, update_func=update_progress_func,
            isnumericfilter=True)
        update_model_state(model_id=model_id, new_progress=0, new_notes="training the model")
        if data is None:
            update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED,
                               new_notes="No data is extracted from the endpoint")
            return
        if np.any(np.isnan(data)):
            print "explore_and_train_tbox> there is a nan in the data"
            print "**************************"
        else:
            print "explore_and_train_tbox> no nans in the data"
        model = learning.train_with_data_and_meta(data=data, meta_data=meta_data, update_func=update_progress_func)
        update_model_state(model_id=model_id, new_progress=0, new_notes="organizing the clusters")
        meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data,
                                                           update_func=update_progress_func)
        # Now I'm not using the computed data here
        # update_model_state(model_id=model_id, new_progress=0, new_notes="computing the score of the trained model")
        # learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters,
        #                                  update_func=update_progress_func)
        update_model_state(model_id=model_id, new_progress=0, new_notes="Saving the model data")
        model_file_name = data_extraction.save_model(model=model, meta_data=meta_data, file_name=str(model_id) + " - ")
        if model_file_name is not None:
            m = MLModel.objects.filter(id=model_id)
            if len(m) == 1:
                m = m[0]
                m.file_name = model_file_name
                m.save()
                update_model_state(model_id=model_id, new_progress=100, new_state=MLModel.COMPLETE, new_notes="Completed")
            else:
                update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED, new_notes="model is deleted")
        else:
            update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED, new_notes="Error Saving the model")
    except Exception as e:
        print "explore_and_train_tbox> Exception %s" % str(e)
        traceback.print_exc()
        update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Not captured error: " + str(e))


def explore_and_train_abox(endpoint=None, model_id=None, classes_uris=[]):
    if endpoint is None:
        print "explore_and_train_abox> endpoint is None"
        return
    if model_id is None:
        print "explore_and_train_abox> model_id should not be None"
        return
    try:
        update_progress_func = partial(update_model_progress_for_partial, model_id)
        update_model_state(model_id=model_id, new_state=MLModel.RUNNING, new_progress=0,
                           new_notes="Extracting numerical class/property combinations")
        classes_properties_uris = []
        for idx, class_uri in enumerate(classes_uris):
            update_progress_func(int(idx * 1.0 / len(classes_uris) * 100))
            # properties = easysparql.get_numerical_properties_for_class_abox(endpoint=endpoint, class_uri=class_uri,
            #                                                                 raiseexception=True)
            properties = easysparql.get_numerical_properties_for_class_abox_using_half_split(endpoint=endpoint,
                                                                                             class_uri=class_uri,
                                                                                             raiseexception=True,
                                                                                             lower_bound=1,
                                                                                             upper_bound=100000,
                                                                                             first_time=True)
            for prop in properties:
                classes_properties_uris.append((class_uri, prop))
        update_progress_func(100)
        update_model_state(model_id=model_id, new_progress=0,
                           new_notes="extracting values from gathered class/property")
        data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
            endpoint=endpoint, class_property_uris=classes_properties_uris, update_func=update_progress_func,
            isnumericfilter=True, min_num_of_objects=4)
        update_model_state(model_id=model_id, new_progress=0, new_notes="training the model")
        if data is None:
            update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED,
                               new_notes="No data is extracted from the endpoint")
            return
        if np.any(np.isnan(data)):
            print "explore_and_train_abox> there is a nan in the data"
            print "**************************"
        else:
            print "explore_and_train_abox> no nans in the data"
        model = learning.train_with_data_and_meta(data=data, meta_data=meta_data, update_func=update_progress_func)
        if model is None:
            update_model_state(model_id=model_id, new_state=MLModel.STOPPED,
                               new_notes="leaning failed as model is None")
            return
        update_model_state(model_id=model_id, new_progress=0, new_notes="organizing the clusters")
        meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data,
                                                           update_func=update_progress_func)
        # Now I'm not using the computed data here
        # update_model_state(model_id=model_id, new_progress=0, new_notes="computing the score of the trained model")
        # learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters,
        #                                  update_func=update_progress_func)
        update_model_state(model_id=model_id, new_progress=0, new_notes="Saving the model data")
        model_file_name = data_extraction.save_model(model=model, meta_data=meta_data, file_name=str(model_id) + " - ")
        if model_file_name is not None:
            m = MLModel.objects.filter(id=model_id)
            if len(m) == 1:
                m = m[0]
                m.file_name = model_file_name
                m.save()
                update_model_state(model_id=model_id, new_progress=100, new_state=MLModel.COMPLETE, new_notes="Completed")
            else:
                update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED, new_notes="model is deleted")
        else:
            update_model_state(model_id=model_id, new_progress=0, new_state=MLModel.STOPPED, new_notes="Error Saving the model")
    except Exception as e:
        print "explore_and_train_abox> Exception %s" % str(e)
        traceback.print_exc()
        update_model_state(model_id=model_id, new_state=MLModel.STOPPED, new_notes="Raised error: " + str(e))


def predict_files(predictionrun_id=None, model_dir=None, files=[], original_uploaded_filenames=[], has_header=False):
    """
    :param predictionrun_id:
    :param model_dir: the dir of the FCM model csv file abs dir
    :param files: list of files to be predicted
    :return:
    """
    if predictionrun_id is None:
        print "predict_files> predictionrun_id should not be None"
        return
    if model_dir is None:
        print "predict_files> model_dir should not be None"
        return
    if len(files) != len(original_uploaded_filenames):
        print "predict_files> number of files (%d) does not equal original_uploaded_filenames (%d)" % \
              (len(files), len(original_uploaded_filenames))
        return
    print "original uploaded files:"
    print original_uploaded_filenames
    update_func = partial(update_predictionrun_progress_for_partial, predictionrun_id)
    update_predictionrun_state(predictionrun_id=predictionrun_id, new_progress=0, new_state=PredictionRun.RUNNING)
    model, types = learning.load_model(model_dir)
    num_of_files = len(files)
    for idx, fname in enumerate(files):
        # update_predictionrun_state(predictionrun_id=predictionrun_id, new_progress=int(idx * 1.0 / num_of_files * 100),
        #                            new_notes='predicting columns in file: ' + fname.split('/')[-1].strip()[:-4])
        update_predictionrun_state(predictionrun_id=predictionrun_id,
                                   new_notes='predicting columns in file: ' + fname.split('/')[-1].strip()[:-4])
        data, meta_data = data_extraction.data_and_meta_from_a_mixed_file(file_name=fname, has_header=has_header,
                                                        original_file_name=original_uploaded_filenames[idx])
        print "predict_files> extracted data shape is %s " % str(data.shape)
        u = learning.predict(model=model, data=data, meta_data=meta_data, update_func=update_func)
        predictionrun = PredictionRun.objects.filter(id=predictionrun_id)
        if len(predictionrun) == 1:
            predictionrun = predictionrun[0]
            file_column_list = [{"file_name": fc["type"].split(' , ')[0], "column_no": fc["type"].split(' , ')[1]}
                                for fc in meta_data]
            predictionrun.add_memberships(u, file_column_list)
        else:
            update_predictionrun_state(predictionrun_id=predictionrun_id,
                                       new_notes="predictionrun_id is not longer exists",
                                       new_state=PredictionRun.STOPPED)
            return
    predictionrun = PredictionRun.objects.filter(id=predictionrun_id)
    if len(predictionrun) == 1:
        predictionrun = predictionrun[0]
        predictionrun.set_types(types)
        print "setting types"
        print types
    else:
        update_predictionrun_state(predictionrun_id=predictionrun_id,
                                   new_notes="predictionrun_id is not longer exists",
                                   new_state=PredictionRun.STOPPED)
        return
    update_predictionrun_state(predictionrun_id=predictionrun_id, new_progress=100, new_state=PredictionRun.COMPLETE,
                               new_notes='')


def get_types_and_membership(predictionrun_id=None, top_k_candidates=5, model_dir=None):
    if model_dir is None:
        print 'get_types_and_membership> model_dir should not be None'
        return []
    if predictionrun_id is None:
        print 'get_types_and_membership> predictionrun_id should not be None'
        return []
    predictionrun = PredictionRun.objects.filter(id=predictionrun_id)
    if len(predictionrun) != 1:
        print 'get_types_and_membership> predictionrun_id is not longer exists'
        return []

    predictionrun = predictionrun[0]
    model, types = learning.load_model(model_dir)
    types = np.array(types)
    list_of_mem_with_types = []
    print 'mem with types'
    for m in Membership.objects.filter(prediction_run=predictionrun):
        mem_with_types = {}
        mems = m.get_values_as_numpy()
        mems_idxs = mems.argsort()[::-1][:5]  # idxs sorted from largest (value not largest index) to smallest
        mems = mems[mems_idxs]
        mems *= 100
        # mem_with_types["types"] = types[mems_idxs].tolist()
        # mem_with_types["scores"] = mems.tolist()
        mem_with_types["typesscores"] = zip(mems.tolist(), types[mems_idxs].tolist())
        mem_with_types["column_no"] = m.column_no
        mem_with_types["file_name"] = m.file_name
        list_of_mem_with_types.append(mem_with_types)
        #print mem_with_types
    return list_of_mem_with_types


####################################################################
#                State update functions                            #
####################################################################


def update_model_progress_for_partial(model_id, new_progress):
    return update_model_state(model_id=model_id, new_progress=new_progress)


def update_model_state(model_id=None, new_state=None, new_notes=None, new_progress=None):
    m = MLModel.objects.filter(id=model_id)
    if len(m) == 1:
        m = m[0]
        if new_state is not None:
            m.state = new_state
        if new_notes is not None:
            m.notes = new_notes
        if new_progress is not None:
            m.progress = new_progress
        m.save()
        return m
    return None


def update_predictionrun_progress_for_partial(predictionrun_id, new_progress):
    return update_predictionrun_state(predictionrun_id=predictionrun_id, new_progress=new_progress)


# def update_predictionrun_notes_for_partial(predictionrun_id, new_notes):
#     return update_predictionrun_state(predictionrun_id=predictionrun_id, new_notes=new_notes)


def update_predictionrun_state(predictionrun_id=None, new_state=None, new_notes=None, new_progress=None):
    m = PredictionRun.objects.filter(id=predictionrun_id)
    if len(m) == 1:
        m = m[0]
        if new_state is not None:
            m.state = new_state
        if new_notes is not None:
            m.notes = new_notes
        if new_progress is not None:
            m.progress = new_progress
        m.save()
        return m
    return None


