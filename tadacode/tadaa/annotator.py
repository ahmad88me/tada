###############################
#       For Django script     #
###############################
import pandas as pd
import numpy as np
import random
import string
import os
import sys

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tadaa.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

#######################################
#       For the annotation script     #
#######################################

from tadaa.models import OnlineAnnotationRun, Cell, CClass, Entity


def annotate_csvs(ann_run_id, files, endpoint, gen_class_eli, hierarchy):
    """
    :param ann_run_id: the id of the annotation run as a string
    :param files: a list of files in abs dir
    :param endpoint: the endpoint url
    :return: Nothing
    """
    from tadaa.models import OnlineAnnotationRun
    try:
        ann_run = OnlineAnnotationRun.objects.get(id=ann_run_id)
    except:
        ann_run = OnlineAnnotationRun(name=random_string(5), status='started')
    for f in files:
        ann_run.status = 'annotating file: ' + str(f.split(os.path.sep)[-1])
        ann_run.save()
        annotate_single_csv(ann_run=ann_run, csv_file=f, endpoint=endpoint, hierarchy=hierarchy)
    # if gen_class_eli:
    #     eliminate_general_classes(ann_run=ann_run, endpoint=endpoint)


def annotate_single_csv(ann_run, csv_file, endpoint, hierarchy):
    """
    Assumptions:
        * Only one entity column i.e. not considering the case of multiple columns for the entity (e.g. the case of
        first name column and last name column).
        * The entity column is the first column.
    :param ann_run:online annotation run
    :param csv_file: the directory of the file
    :param endpoint: the endpoint url
    :return:
    """
    print 'annotating: ' + csv_file
    mat = pd.read_csv(csv_file).as_matrix()
    # Here we assume that the entity column is the first one
    # get entity column
    entity_column_id = 0
    for r in mat:
        annotate_single_cell(ann_run=ann_run, cell_value=r[entity_column_id], endpoint=endpoint, hierarchy=hierarchy)


def annotate_single_cell(ann_run, cell_value, endpoint, hierarchy):
    from easysparql import get_entities, get_classes
    cell = Cell(text_value=cell_value, annotation_run=ann_run)
    cell.save()
    for entity in get_entities(subject_name=cell.text_value, endpoint=endpoint):
        entity = Entity(cell=cell, entity=entity)
        entity.save()
        for c in get_classes(entity=entity.entity, endpoint=endpoint, hierarchy=hierarchy):
            print c
            cclass = CClass(entity=entity, cclass=c)
            cclass.save()


def eliminate_general_classes(ann_run, endpoint):
    from easysparql import get_classes_not_in
    classes = []
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                classes.append(cclass.cclass)
    classes = list(set(classes))
    s_classes = get_classes_not_in(classes=classes, endpoint=endpoint)
    if len(s_classes) == 0:
        print "No classes is returned"
        return
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                if cclass.cclass not in s_classes:
                    cclass.delete()


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


if __name__ == '__main__':
    for idx, a in enumerate(sys.argv):
        print '%d => %s' % (idx, a)
    if len(sys.argv) == 2:
        from tadaa.models import OnlineAnnotationRun
        ann_run = OnlineAnnotationRun.objects.get(id=sys.argv[1])
        print "eliminating classes"
        eliminate_general_classes(ann_run=ann_run, endpoint="http://dbpedia.org/sparql")
        print "classes eliminated"
    elif len(sys.argv) < 5:
        print "annotator expects the run id and list of files to be annotated"
    elif sys.argv[1] not in ['true', 'false']:
        print sys.argv[1]
        print "second argument must be true or false to indicate whether general classes elimenation is enabled or not"
    elif sys.argv[2] not in ['true', 'false']:
        print sys.argv[2]
        print "third argument must be true or false to indicate whether the classes hierarchy is included"
    else:
        files = sys.argv[4:]
        annotate_csvs(ann_run_id=sys.argv[3], hierarchy=sys.argv[2] == 'true', files=files,
                      gen_class_eli=sys.argv[1] == 'true', endpoint="http://dbpedia.org/sparql")
        print "Annotation is completed"
