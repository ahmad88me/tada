###############################
#       For Django script     #
###############################

import numpy as np
import random
import string
import os
import sys
import math

#MAX_NUM_PROCESSES = 10
MAX_NUM_PROCESSES = 1

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

from settings import MODELS_DIR, LOG_ABS_DIR
from django.core.files import File
from django.core.files.base import ContentFile
from tadaa.models import AnnRun, EntityAnn, Cell, CClass, Entity
import argparse
import json

import time
import logging

from multiprocessing import Process, Lock, Pipe
from PPool.Pool import Pool
import multiprocessing
#from multiprocessing import Pool
from type_graph import TypeGraph

from logger import set_config


logger = set_config(logging.getLogger(__name__), logdir=os.path.join(LOG_ABS_DIR, 'tada.log'))


def detect_entity_col(csv_file_dir):
    """
    :param csv_file_dir:
    :return: the index of the entity column, or -1 if it is can't be found
    """
    return 0  # at the moment we assume that the entity column is the first column


def annotate_csv(ann_run_id, csv_file_dir, endpoint, hierarchy, entity_col_id, onlyprefix):
    """
    Assumptions:
        * Only one entity column i.e. not considering the case of multiple columns for the entity (e.g. the case of
        first name column and last name column).
    :param ann_run_id:
    :param csv_file_dir:
    :param endpoint:
    :param hierarchy:
    :param entity_col_id: the id the column id
    :return:
    """
    import pandas as pd
    if entity_col_id is None:
        entity_column_id = detect_entity_col(csv_file_dir)
    else:
        entity_column_id = entity_col_id
    try:
        ann_run = AnnRun.objects.get(id=ann_run_id)
    except:
        ann_run = AnnRun(name=random_string(5), status='started')
    ann_run.status = 'adding dataset: ' + str(csv_file_dir.split(os.path.sep)[-1])
    ann_run.save()
    print "ann_run: "+str(ann_run.id)
    print "how many entityAnns: "+str(len(EntityAnn.objects.filter(ann_run=ann_run)))
    print "on reverse: "+str(len(ann_run.entityann_set.all()))
    # for ea in EntityAnn.objects.filter(ann_run=ann_run):
    #     print "deleting ea with id: "+str(ea.id)
    #     ea.delete()
    EntityAnn.objects.filter(ann_run=ann_run).delete()
    entity_ann = EntityAnn(ann_run=ann_run, col_id=entity_column_id)
    entity_ann.save()
    start = time.time()
    logger.info('annotating: ' + csv_file_dir)
    mat = pd.read_csv(csv_file_dir).as_matrix()
    params_list = []
    for r in mat:
        params_list.append((entity_ann, r[entity_column_id], endpoint, hierarchy, onlyprefix))
    pool = Pool(max_num_of_processes=MAX_NUM_PROCESSES, func=annotate_single_cell, params_list=params_list)
    pool.run()
    end = time.time()
    logger.debug("Time spent: %f" % (end-start))
    ann_run.status = 'datasets are added'
    ann_run.save()


def annotate_single_cell(entity_ann, cell_value, endpoint, hierarchy, onlyprefix):
    from easysparql import get_entities, get_classes
    print "annotate_single_cell> "
    print "entity_ann parent name: "
    print entity_ann.ann_run.name
    cell = Cell(text_value=cell_value, entity_ann=entity_ann)
    cell.save()
    logger.debug("cell: "+str(cell_value))
    for entity in get_entities(subject_name=cell.text_value, endpoint=endpoint):
        logger.debug("entity: "+str(entity))
        e = Entity(cell=cell, entity=entity)
        e.save()
        logger.debug("will get classes of: " + entity)
        classes = get_classes(entity=entity, endpoint=endpoint, hierarchy=hierarchy)
        for c in classes:
            if onlyprefix is None or (c.startswith(onlyprefix)):
                ccclass = CClass(entity=e, cclass=c)
                ccclass.save()


def build_graph_while_traversing(class_name, endpoint, v_lock, v_pipe, depth, onlyprefix):
    """
    :param class_name:
    :param endpoint:
    :param g_lock:
    :param v_lock:
    :param g_pipe:
    :param v_pipe:
    :param depth:
    :param onlyprefix: filter to only classes that starts with it
    :return:
    """
    print "class_name: %s depth: %d" % (class_name, depth)
    from easysparql import get_parents_of_class
    v_lock.acquire()
    v_pipe.send(1)
    visited = v_pipe.recv()
    v_lock.release()

    if class_name not in visited:
        parents = get_parents_of_class(class_name=class_name, endpoint=endpoint)
        v_lock.acquire()
        v_pipe.send(1)
        visited = v_pipe.recv()
        if onlyprefix is None:
            filtered_parents = parents
        else:
            filtered_parents = [p for p in parents if p.startswith(onlyprefix)]
        visited[class_name] = filtered_parents
        v_pipe.send(visited)
        v_lock.release()

        for p in filtered_parents:
            build_graph_while_traversing(class_name=p, endpoint=endpoint, v_lock=v_lock, v_pipe=v_pipe, depth=depth+1,
                                         onlyprefix=onlyprefix)


def build_graph_from_nodes(graph, nodes_dict):
    """
    :param graph:
    :param nodes_dict: each node (key) contains a list of its parents
    :return:
    """
    logger.debug("adding nodes")
    # add nodes
    for node in nodes_dict:
        graph.add_v(node, None)

    logger.debug("all nodes are added")
    # add edges

    logger.debug("adding edges")
    for node in nodes_dict:
        for p in nodes_dict[node]:
            graph.add_e(p, node)
    logger.debug("all edges are added")
    graph.build_roots()
    logger.debug("roots are built\n\n***\n\n\n\n\n***********")
    # graph.draw("graph-pre.gv")
    logger.debug("will break the cycles")
    graph.break_cycles(log_path=proj_path)
    logger.debug("cycles are broken")


def compute_coverage_score_for_graph(entity_ann, graph):
    for cell in entity_ann.cells:
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
                if n is None:
                    print "couldn't find %s" % cclass.cclass
                n.coverage_score += c_score


def v_writer_func(visited, pipe):
    v = None
    while True:
        v = pipe.recv()
        if v == 1:
            pipe.send(visited)
        else:
            visited = v


def count_classes_writer_func(pipe):
    d = {}
    while True:
        v = pipe.recv()
        if v == 1:
            pipe.send(d)
        else:
            k = v.keys()[0]
            d[k] = v[k]


def count_classes_func(c, endpoint, lock, pipe):
    from easysparql import get_classes_subjects_count
    d = get_classes_subjects_count(c, endpoint)
    lock.acquire()
    pipe.send(d)
    lock.release()


def count_classes(classes, endpoint):
    """
    count classes from a given endpoint using a pool of processes
    :param classes:
    :param endpoint:
    :return:
    """
    print "in count classes"
    from multiprocessing import Process, Lock, Pipe

    lock = Lock()
    a_end, b_end = Pipe()

    print "in count classes> the writer process"
    writer_process = Process(target=count_classes_writer_func, args=(a_end,))
    writer_process.start()

    print "in count classes> preparing the pool"
    param_list = [([c], endpoint, lock, b_end) for c in classes]
    pool = Pool(max_num_of_processes=MAX_NUM_PROCESSES, func=count_classes_func, params_list=param_list)
    pool.run()
    print "pool run if finished"

    print "sending 1"
    b_end.send(1)
    print "waiting to receive"
    d = b_end.recv()
    print "received"
    writer_process.terminate()
    print "in count classes> returns :%s" % str(d)
    return d


def remove_nodes(entity_ann, classes):
    for cell in entity_ann.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                if cclass.cclass in classes:
                    CClass.objects.get(cclass=cclass.cclass, entity=entity).delete()


def remove_empty(entity_ann):
    for cell in entity_ann.cells:
        for entity in cell.entities:
            if len(entity.classes) == 0:
                Entity.objects.get(id=entity.id).delete()


def remove_noise_entities(entity_ann):
    for cell in entity_ann.cells:
        if len(cell.entities) >= 2:
            max_num = 0
            for entity in cell.entities:
                num_classes = len(entity.classes)
                if num_classes > max_num:
                    max_num = num_classes
            num_classes_limit = math.sqrt(max_num)
            for entity in cell.entities:
                if len(entity.classes) < num_classes_limit:
                    entity.delete()


def get_m(entity_ann):
    """
    :param ann_run:
    :return: number of cells that has entities
    """
    s = 0
    for cell in entity_ann.cells:
        if len(cell.entities) !=0:
            s+=1
    if s!=0:
        return s * 1.0
    return 1.0


def store_scores(ann_run,scores):
    """
    :param scores: a list of tuples in the form of score, type url order by most probable types
    :return:
    """
    ann_run.results = ""
    for uri in scores[:5]:
        ann_run.results += uri[-99:] + ","
    ann_run.save()


def dotype(ann_run, endpoint, onlyprefix):
    ann_run.status = 'removing noisy entities'
    ann_run.save()
    entity_ann = ann_run.entityann_set.all()[0]
    remove_noise_entities(entity_ann)
    ann_run.status = 'subclass queries'
    ann_run.save()
    timed_events = []
    graph = TypeGraph()
    params = []

    v_lock = Lock()
    v_reader_end, v_writer_end = Pipe()
    v_writer_process = Process(target=v_writer_func, args=({}, v_writer_end))
    v_writer_process.start()

    collected_classes = []

    for cell in entity_ann.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                if cclass.cclass not in collected_classes:
                    if onlyprefix is None or (onlyprefix is not None and cclass.cclass.startswith(onlyprefix)):
                        params.append((cclass.cclass, endpoint, v_lock, v_reader_end, 0, onlyprefix))
                        collected_classes.append(cclass.cclass)
    start = time.time()
    pool = Pool(max_num_of_processes=MAX_NUM_PROCESSES, func=build_graph_while_traversing, params_list=params)
    logger.debug("will run the pool")
    pool.run()
    logger.debug("the pool is done")
    end = time.time()
    timed_events.append(("build graph while traversing", end-start))
    v_reader_end.send(1)
    visited = v_reader_end.recv()
    v_writer_process.terminate()
    logger.debug("build graph from nodes\n\n")
    ann_run.status = 'building the class graph'
    ann_run.save()
    start = time.time()
    build_graph_from_nodes(graph=graph, nodes_dict=visited)
    end = time.time()
    timed_events.append(("build graph2", end-start))
    logger.debug("remove single nodes\n\n")
    start = time.time()
    remove_nodes(entity_ann=entity_ann, classes=graph.remove_lonely_nodes())
    end = time.time()
    timed_events.append(("remove lonely nodes", end-start))
    start = time.time()
    remove_empty(entity_ann=entity_ann)
    end = time.time()
    timed_events.append(("remove empty entities", end - start))
    logger.debug("coverage\n\n")
    ann_run.status = 'Computing the coverage scores'
    ann_run.save()
    start = time.time()
    compute_coverage_score_for_graph(entity_ann=entity_ann, graph=graph)
    graph.set_converage_score()
    end = time.time()
    timed_events.append(("coverage", end-start))
    ann_run.status = 'Performing count queries'
    ann_run.save()
    logger.debug("count subjects \n\n")
    start = time.time()
    classes_counts = count_classes(classes=graph.cache, endpoint=endpoint)

    graph.set_nodes_subjects_counts(d=classes_counts)
    end = time.time()
    timed_events.append(("classes counts", end-start))
    logger.debug("specificity\n\n")
    ann_run.status = 'Computing the specificity scores'
    ann_run.save()

    start = time.time()
    graph.set_specificity_score()
    graph.set_path_specificity()
    end = time.time()
    timed_events.append(("specificity", end-start))
    start = time.time()
    graph.set_depth_for_graph()
    graph.set_score_for_graph(coverage_weight=0.1, m=get_m(entity_ann))
    end = time.time()
    timed_events.append(("latest score", end-start))
    ann_run.status = 'Computing the overall scores'
    ann_run.save()

    latest_scores = graph.get_scores()
    store_scores(ann_run, [n.title for n in latest_scores])
    print "scores: "
    for n in latest_scores:
        print "%f %s" % (n.score, n.title)
    for te in timed_events:
        print "event: %s took: %.2f seconds" % (te[0], te[1])
    graph_file_name = "%d %s.json" % (ann_run.id, ann_run.name)
    graph_file_name = graph_file_name.replace(' ', '_')
    graph_file_dir = os.path.join(MODELS_DIR, graph_file_name)
    logger.debug("graph_file_dir: "+graph_file_dir)
    graph.save(graph_file_dir)
    #entity_ann.graph_file.name = graph_file_dir
    entity_ann.save()
    ann_run.status = 'Annotation is complete'
    ann_run.save()


def load_graph(entity_ann):
    from type_graph import TypeGraph
    f = open(entity_ann.graph_file.path, 'r')
    j = json.loads(f.read())
    g = TypeGraph()
    g.load(j, get_m(entity_ann))
    return g


def score_graph(graph, alpha, entity_ann):
    graph.set_score_for_graph(coverage_weight=alpha, m=get_m(entity_ann))
    return [n.title for n in graph.get_scores()]


def get_nodes(graph):
    return [graph.index[t] for t in graph.cache]
    # return graph.cache


def get_edges(graph):
    return graph.get_edges()


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


if __name__ == '__main__':
    global logger
    endpoint = "http://dbpedia.org/sparql"
    parser = argparse.ArgumentParser(description='Annotation module to annotate a given annotation run')
    parser.add_argument('runid', type=int, metavar='Annotation_Run_ID', help='the id of the Annotation Run ')
    parser.add_argument('--csvfiles', action='append', nargs='+', help='the list of csv files to be annotated')
    parser.add_argument('--dotype', action='store_true', help='To conclude the type/class of the given csv file')
    parser.add_argument('--onlyprefix', action='store', help='To limit to classes that starts with this prefix')
    parser.add_argument('--entitycol', type=int, action='store', help='The id of the entity column in the csv file')
    parser.add_argument('--logdir', action='store', help='suffix to the log file')
    args = parser.parse_args()
    if args.logdir:
        logger = set_config(logging.getLogger(__name__), logdir=args.logdir)
    if args.csvfiles and len(args.csvfiles) > 0:
        logger.debug('csvfiles: %s' % args.csvfiles)
        logger.debug("adding dataset")
        logger.debug("csv_file_dir: ")
        logger.debug(args.csvfiles[0])
        prefix = None
        if args.onlyprefix:
            prefix = args.onlyprefix
        annotate_csv(ann_run_id=args.runid, hierarchy=False, csv_file_dir=args.csvfiles[0][0],
                     endpoint="http://dbpedia.org/sparql", entity_col_id=args.entitycol, onlyprefix=prefix)
        logger.info("data set is added successfully.")
    if args.dotype:
        prefix = None
        # The hierarchy is not restricted to the passed prefix
        # if args.onlyprefix:
        #     prefix = args.onlyprefix
        ann_run = AnnRun.objects.get(id=args.runid)
        logger.debug('typing the csv file')
        dotype(ann_run=ann_run, endpoint=endpoint, onlyprefix=prefix)
        logger.info('done typing the csv file')
