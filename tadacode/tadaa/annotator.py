###############################
#       For Django script     #
###############################
import pandas as pd
import numpy as np
import random
import string
import os
import sys
import math

MAX_NUM_PROCESSES = 10

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
    import time
    from ppool import Pool
    from multiprocessing import Lock, Pipe, Process
    start = time.time()
    print 'annotating: ' + csv_file
    mat = pd.read_csv(csv_file).as_matrix()
    # Here we assume that the entity column is the first one
    # get entity column
    entity_column_id = 0
    # for r in mat:
    #     annotate_single_cell(ann_run=ann_run, cell_value=r[entity_column_id], endpoint=endpoint, hierarchy=hierarchy)
    params_list = []
    lock = Lock()
    a_end, b_end = Pipe()

    v_writer_process = Process(target=annotation_writer_func, args=(b_end,))
    v_writer_process.start()

    for r in mat:
        params_list.append((ann_run, r[entity_column_id], endpoint, hierarchy, lock, a_end))
    pool = Pool(max_num_of_processes=MAX_NUM_PROCESSES, func=annotate_single_cell, params_list=params_list)
    pool.run()
    print "sending 1"
    a_end.send(1)
    print "will ask for the dict list"
    dict_list = a_end.recv()
    print "received the dict list"
    annotation_write_to_db(dict_list)
    print "1 is sent"
    v_writer_process.terminate()
    end = time.time()
    print "Time spent: %f" % (end-start)


def annotation_writer_func(pipe):
    dict_list = []
    while True:
        v = pipe.recv()
        if v == 1:
            print "annotation_writer_func> will return"
            pipe.send(dict_list)
        else:
            print "annotation_writer_func> will append"
            dict_list.append(v)
            print "annotation_writer_func> appended"


def annotation_write_to_db(dict_list):
    for d in dict_list:
        for cell_value in d.keys():
            cell = Cell(text_value=cell_value, annotation_run=d[cell_value]["ann_run"])
            cell.save()
            for entity_value in d[cell_value]["entities"].keys():
                entity = Entity(cell=cell, entity=entity_value)
                entity.save()
                for class_value in d[cell_value]["entities"][entity_value]:
                    cclass = CClass(entity=entity, cclass=class_value)
                    cclass.save()


def annotate_single_cell(ann_run, cell_value, endpoint, hierarchy, lock, pipe):
    from easysparql import get_entities, get_classes
    dcell = {}
    #lock.acquire()
    cell = Cell(text_value=cell_value, annotation_run=ann_run)
    #cell.save()
    #lock.release()
    dcell[cell_value] = {"ann_run": ann_run, "entities": {}}
    print "cell: "+cell_value
    for entity in get_entities(subject_name=cell.text_value, endpoint=endpoint):
        #lock.acquire()
        #entity = Entity(cell=cell, entity=entity)
        #entity.save()
        #entity_string = entity.entity
        #lock.release()
        dcell[cell_value]["entities"][entity] = []
        classes = get_classes(entity=entity, endpoint=endpoint, hierarchy=hierarchy)
        #lock.acquire()
        print "entity: "+entity
        for c in classes:
            #print c
            #cclass = CClass(entity=entity, cclass=c)
            #cclass.save()
            dcell[cell_value]["entities"][entity].append(c)
        #lock.release()
    print "will acquire"
    lock.acquire()
    print "sending ..."
    pipe.send(dcell)
    print "send"
    lock.release()
    print "release"


def build_graph_while_traversing(class_name, endpoint, v_lock, v_pipe, depth=0):
    """
    :param class_name:
    :param endpoint:
    :param g_lock:
    :param v_lock:
    :param g_pipe:
    :param v_pipe:
    :param depth:
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
        visited[class_name] = parents
        v_pipe.send(visited)
        v_lock.release()

        for p in parents:
            build_graph_while_traversing(class_name=p, endpoint=endpoint, v_lock=v_lock, v_pipe=v_pipe, depth=depth+1)


def build_graph_from_nodes(graph, nodes_dict):
    """
    :param graph:
    :param nodes_dict: each node (key) contains a list of its parents
    :return:
    """
    print "adding nodes"
    # add nodes
    for node in nodes_dict:
        graph.add_v(node, None)

    print "all nodes are added"
    # add edges

    print "adding edges"
    for node in nodes_dict:
        for p in nodes_dict[node]:
            graph.add_e(p, node)
    print "all edges are added"
    graph.build_roots()
    print "roots are built\n\n***\n\n\n\n\n***********"
    #graph.draw("graph-pre.gv")
    print "will break the cycles"
    graph.break_cycles()
    print "cycles are broken"


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
    from ppool import Pool

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


def remove_nodes(ann_run, classes):
    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                if cclass.cclass in classes:
                    CClass.objects.get(cclass=cclass.cclass, entity=entity).delete()


def remove_empty(ann_run):
    for cell in ann_run.cells:
        for entity in cell.entities:
            if len(entity.classes) == 0:
                Entity.objects.get(id=entity.id).delete()


def remove_noise_entities(ann_run):
    for cell in ann_run.cells:
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


def dotype(ann_run, endpoint):
    import time
    from multiprocessing import Process, Lock, Pipe
    from ppool import Pool
    from easysparql import get_classes_subjects_count
    from basic_graph import BasicGraph
    remove_noise_entities(ann_run)

    timed_events = []
    graph = BasicGraph()
    params = []
    processes = []
    v_lock = Lock()
    v_reader_end, v_writer_end = Pipe()
    v_writer_process = Process(target=v_writer_func, args=({}, v_writer_end))
    v_writer_process.start()

    for cell in ann_run.cells:
        for entity in cell.entities:
            for cclass in entity.classes:
                params.append((cclass.cclass, endpoint, v_lock, v_reader_end))
    start = time.time()
    pool = Pool(max_num_of_processes=MAX_NUM_PROCESSES, func=build_graph_while_traversing, params_list=params)
    print "will run the pool"
    pool.run()
    print "the pool is done"
    end = time.time()
    timed_events.append(("build graph while traversing", end-start))
    v_reader_end.send(1)
    visited = v_reader_end.recv()
    v_writer_process.terminate()

    for k in visited:
        print "[%s] =>" % k
        print "\t\t %s" % ",".join(visited[k])

    print "\n\n\n\n"
    print "build graph from nodes\n\n"
    start = time.time()
    build_graph_from_nodes(graph=graph, nodes_dict=visited)
    end = time.time()
    timed_events.append(("build graph2", end-start))
    print "remove nodes\n\n"
    start = time.time()
    remove_nodes(ann_run=ann_run, classes=graph.remove_lonely_nodes())
    end = time.time()
    timed_events.append(("remove lonely nodes", end-start))
    #graph.draw("graph-post.gv")
    start = time.time()
    remove_empty(ann_run=ann_run)
    end = time.time()
    timed_events.append(("remove empty entities", end - start))
    print "coverage\n\n"
    start = time.time()
    compute_coverage_score_for_graph(ann_run=ann_run, graph=graph)
    graph.set_converage_score()
    end = time.time()
    timed_events.append(("coverage", end-start))

    print "count subjects \n\n"
    # iteration 8
    start = time.time()
    print "inside == will count classes"
    classes_counts = count_classes(classes=graph.cache, endpoint=endpoint)
    print "outside == after classes are counted"
    graph.set_nodes_subjects_counts(d=classes_counts)
    end = time.time()
    timed_events.append(("classes counts", end-start))

    print "specificity\n\n"
    start = time.time()
    graph.set_specificity_score()
    graph.set_path_specificity()
    end = time.time()
    timed_events.append(("specificity", end-start))
    start = time.time()
    graph.set_score_for_graph(0.01)
    end = time.time()
    timed_events.append(("latest score", end-start))
    print "scores: "
    for n in graph.get_scores():
        print "%f %s" % (n.score, n.title)
    for te in timed_events:
        print "event: %s took: %.2f seconds" % (te[0], te[1])
    graph.draw_with_scores()


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


if __name__ == '__main__':
    endpoint = "http://dbpedia.org/sparql"
    parser = argparse.ArgumentParser(description='Annotation module to annotate a given annotation run')
    parser.add_argument('runid', type=int, metavar='Annotation_Run_ID', help='the id of the Annotation Run ')
    parser.add_argument('--dotype', action='store_true', help='To conclude the type/class of the given csv file')
    args = parser.parse_args()
    if args.csvfiles and len(args.csvfiles) > 0:
        print 'csvfiles: %s' % args.csvfiles
        print "annotation started"
        annotate_csvs(ann_run_id=args.runid, hierarchy=False, files=args.csvfiles[0], gen_class_eli=False,
                      endpoint="http://dbpedia.org/sparql")
        print "annotation is done"
    if args.dotype:
        ann_run = OnlineAnnotationRun.objects.get(id=args.runid)
        print 'typing the csv file'
        dotype(ann_run=ann_run, endpoint=endpoint)
        print 'done typing the csv file'
