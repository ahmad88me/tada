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
import argparse


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


def omit_root_classes(ann_run, endppoint):
    """
    To delete types that does not have a parent. This is to solve the problem with classes
    :param ann_run:
    :param endppoint:
    :return:
    """
    from easysparql import get_classes_with_parents
    classes = []
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                classes.append(cclass.cclass)
    classes = list(set(classes))
    classes_with_parents = get_classes_with_parents(classes=classes, endpoint=endpoint)
    if len(classes_with_parents) == 0:
        print "No classes with parents are returned"
        return
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                if cclass.cclass not in classes_with_parents:
                    cclass.delete()


def build_class_graph_with_score(ann_run, endpoint):
    from basic_graph import BasicGraph
    graph = BasicGraph()
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                build_graph_while_traversing(class_name=cclass.cclass, graph=graph, endpoint=endpoint)
    for cell in ann_run.cells:
        if len(cell.entities) == 0:
            e_score = 0
        else:
            e_score = 1.0 / len(cell.entities)
        for entity in cell.entities:
            if len(entity.classes) == 0:
                c_score = 0
            else:
                c_score = 1.0 / len(entity.classes)
            for cclass in entity.classes:
                n = graph.find_v(cclass.cclass)
                n.coverage_score += c_score
    graph.draw_with_scores()


def build_class_graph(ann_run, endpoint):
    from basic_graph import BasicGraph
    graph = BasicGraph()
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                build_graph_while_traversing(class_name=cclass.cclass, graph=graph, endpoint=endpoint)
    graph.draw()


def build_graph_while_traversing(class_name, graph, endpoint):
    """
    :param class_name:
    :param graph:
    :param endpoint:
    :return:
    """
    from easysparql import get_parents_of_class
    parents = get_parents_of_class(class_name=class_name, endpoint=endpoint)
    for p in parents:
        build_graph_while_traversing(class_name=p, graph=graph, endpoint=endpoint)
    graph.add_v(title=class_name, parents=parents)


def compute_coverage_score_for_graph(ann_run, graph):
    for cell in ann_run.cells:
        if len(cell.entities) == 0:
            e_score = 0
        else:
            e_score = 1.0 / len(cell.entities)
        for entity in cell.entities:
            if len(entity.classes) == 0:
                c_score = 0
            else:
                c_score = 1.0 / len(entity.classes)
            for cclass in entity.classes:
                n = graph.find_v(cclass.cclass)
                n.coverage_score += c_score


def dotype(ann_run, endpoint):
    from easysparql import get_classes_subjects_count
    from basic_graph import BasicGraph
    graph = BasicGraph()
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                build_graph_while_traversing(class_name=cclass.cclass, graph=graph, endpoint=endpoint)
    compute_coverage_score_for_graph(ann_run=ann_run, graph=graph)
    graph.set_converage_score()
    # see iteration 6 and 7
    # classes_counts = get_classes_subjects_count(classes=graph.cache, endpoint=endpoint)
    # graph.set_nodes_subjects_counts(classes_counts)
    # graph.set_specificity_score()
    # graph.draw_with_scores()

    # see iteration 8
    # leaves = graph.get_leaves_from_graph()
    # classes_counts = get_classes_subjects_count(classes=[l.title for l in leaves], endpoint=endpoint)
    # graph.set_nodes_subjects_counts(d=classes_counts, leaves=leaves)

    # iteration 8
    classes_counts = get_classes_subjects_count(classes=graph.cache, endpoint=endpoint)
    graph.set_nodes_subjects_counts(d=classes_counts)

    graph.set_specificity_score()
    graph.draw_with_scores()


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


if __name__ == '__main__':
    endpoint = "http://dbpedia.org/sparql"
    parser = argparse.ArgumentParser(description='Annotation module to annotate a given annotation run')
    parser.add_argument('runid', type=int, metavar='Annotation_Run_ID', help='the id of the Annotation Run ')
    parser.add_argument('--eliminateclasses', action='store_true', help='eliminate classes that are too general')
    parser.add_argument('--csvfiles', action='append', nargs='+', help='the list of csv files to be annotated')
    parser.add_argument('--omitrootclasses', action='store_true', help='omit root classes that does not have parent')
    parser.add_argument('--buildgraph', action='store_true', help='To build a class/type hierarchy tree/graph')
    parser.add_argument('--buildgraphscore', action='store_true',
                        help='To build a class/type hierarchy tree/graph with score')
    parser.add_argument('--dotype', action='store_true', help='To conclude the type/class of the given csv file')
    args = parser.parse_args()
    if args.eliminateclasses:
        from tadaa.models import OnlineAnnotationRun
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print "eliminating classes"
        eliminate_general_classes(ann_run=ann_run, endpoint=endpoint)
        print "classes eliminated"
    elif args.csvfiles and len(args.csvfiles) > 0:
        print 'csvfiles: %s' % args.csvfiles
        print "annotation started"
        annotate_csvs(ann_run_id=args.runid, hierarchy=True, files=args.csvfiles[0], gen_class_eli=False,
                      endpoint="http://dbpedia.org/sparql")
        print "annotation is done"
    elif args.omitrootclasses:
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print 'omitting classes with no parent'
        omit_root_classes(ann_run=ann_run, endppoint=endpoint)
        print 'ommiting of root classes is done'
    elif args.buildgraph:
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print 'building class graph'
        build_class_graph(ann_run=ann_run, endpoint=endpoint)
        print 'class graph is built'
    elif args.buildgraphscore:
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print 'building class graph with score'
        build_class_graph_with_score(ann_run=ann_run, endpoint=endpoint)
        print 'class graph with score is built'
    elif args.dotype:
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print 'typing the csv file'
        dotype(ann_run=ann_run, endpoint=endpoint)
        print 'done typing the csv file'
