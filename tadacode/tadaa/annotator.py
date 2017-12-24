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


def annotate_csvs(ann_run_id, files, endpoint):
    """
    :param ann_run_id: the id of the annotation run as a string
    :param files: a list of files in abs dir
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
        annotate_single_csv(ann_run=ann_run, csv_file=f, endpoint=endpoint)


def annotate_single_csv(ann_run, csv_file, endpoint):
    """
    Assumptions:
        * Only one entity column i.e. not considering the case of multiple columns for the entity (e.g. the case of
        first name column and last name column).
        * The entity column is the first column.
    :param ann_run:online annotation run
    :param csv_file: the directory of the file
    :return:
    """
    print 'annotating: ' + csv_file
    mat = pd.read_csv(csv_file).as_matrix()
    # Here we assume that the entity column is the first one
    # get entity column
    entity_column_id = 0
    for r in mat:
        annotate_single_cell(ann_run, r[entity_column_id], endpoint=endpoint)


def annotate_single_cell(ann_run, cell_value, endpoint):
    from easysparql import get_entities, get_classes
    cell = Cell(text_value=cell_value, annotation_run=ann_run)
    cell.save()
    for entity in get_entities(subject_name=cell.text_value, endpoint=endpoint):
        entity = Entity(cell=cell, entity=entity)
        entity.save()
        for c in get_classes(entity=entity.entity, endpoint=endpoint):
            print c
            cclass = CClass(entity=entity, cclass=c)
            cclass.save()


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "annotator expects the run id and list of files to be annotated"
    else:
        files = sys.argv[2:]
        annotate_csvs(sys.argv[1], files, endpoint="http://dbpedia.org/sparql")
