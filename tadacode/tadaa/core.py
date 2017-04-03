
import numpy as np
import easysparql
import data_extraction
import learning

from models import MLModel

QUERY_LIMIT = "LIMIT 100"


def explore(endpoint=None, model_id=None):
    if endpoint is None:
        print "explore> endpoint is None"
        return
    if model_id is None:
        print "explore> model_id should not be None"
        return
    classes_properties_uris = easysparql.get_all_classes_properties_numerical(endpoint=endpoint)
    update_model_state(model_id=model_id, new_progress=30, new_notes="extracted all class/property numerical combinations")
    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(class_property_uris=classes_properties_uris)
    update_model_state(model_id=model_id, new_progress=40, new_notes="extracted meta_data")
    if np.any(np.isnan(data)):
        print "there is a nan in the data"
        print "**************************"
    else:
        print "no nans in the data"
    # data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    update_model_state(model_id=model_id, new_progress=60, new_notes="trained the model")
    meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    update_model_state(model_id=model_id, new_progress=70, new_notes="extract clusters from meta")
    #print "model num_of_clusters: %d" % model.n_clusters
    #print "cluster centers: %s" % str(model.cluster_centers_)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)
    update_model_state(model_id=model_id, new_progress=100, new_notes="Completed")


def update_model_state(model_id=None, new_status=None, new_notes=None, new_progress=None):
    m = MLModel.objects.filter(id=model_id)
    if len(m) != 0:
        m = m[0]
        if new_status is not None:
            m.status = new_status
        if new_notes is not None:
            m.notes = new_notes
        if new_progress is not None:
            m.progress = new_progress
        m.save()
        return m
    return None
