from collections import Counter
from django.shortcuts import render, redirect
from models import EntityAnn, AnnRun


def e_ann_list(request):
    return render(request, 'e_ann_list.html', {'eanns': EntityAnn.objects.all()})


def entity_ann_results(request):
    annotation = EntityAnn.objects.get(id=request.GET['id'].strip())
    return render(request, 'entity_ann_results.html', {'classes': annotation.results.split(',')})


def entity_ann_raw_results(request):
    annotation = EntityAnn.objects.get(id=request.GET['id'].strip())
    return render(request, 'entity_ann_raw_results.html', {'entity_ann': annotation})


def entity_ann_recompute(request):
    eanns = EntityAnn.objects.all()
    if 'id' not in request.GET or 'alpha' not in request.GET:
        if len(eanns) > 0:
            return render(request, 'entity_ann_recompute.html', {'anns': eanns, 'alpha': 0.1, 'selected': eanns[0].id})
        else:
            return render(request, 'entity_ann_recompute.html', {'anns': eanns, 'alpha': 0.1, 'selected': 0})
    else:
        from annotator import load_graph, score_graph, get_nodes, get_edges
        alpha = float(request.GET['alpha'])
        entity_ann = EntityAnn.objects.get(id=request.GET['id'])
        graph = load_graph(entity_ann=entity_ann)
        results = score_graph(entity_ann=entity_ann, alpha=alpha, graph=graph)
        #graph.draw_with_scores()
        return render(request, 'entity_ann_recompute.html',
                      {'anns': eanns, 'alpha': alpha, 'network': 'network',
                       'highlights': results[:3], 'nodes': get_nodes(graph), 'edges': get_edges(graph),
                       'results': results, 'selected': entity_ann.id})


def live_monitor(request):
    statuses = [s.status for s in AnnRun.objects.all()]
    c = Counter(statuses)
    return render(request, 'live_monitor.html', {'counters': dict(c)})


def about(request):
    return render(request, 'about.html')

# import os
# import string
# import random
# from collections import Counter
#
# import settings
# from django.http import JsonResponse
# from models import MLModel, PredictionRun, Membership, OnlineAnnotationRun, Cell, Entity
# import core
# from django.views.generic import View
# import subprocess
#
#
#
#
# def get_classes(request):
#     if request.method != 'POST':
#         print "method is not POST"
#         print "method is: %s" % request.method
#         return JsonResponse({'status': False, 'message': 'method should be POST'})
#     else:
#         endpoint = request.POST['endpoint']
#         classes = core.get_classes(endpoint=endpoint)
#         return JsonResponse({'status': True, 'classes': classes})
#
#
# def add_model_abox(request):
#     if request.method == 'GET':
#         return render(request, 'add_model_abox.html')
#     elif request.method == 'POST':
#         error_msg = ''
#         if 'url' not in request.POST:
#             error_msg = 'url is not passed'
#         if 'name' not in request.POST:
#             error_msg = 'name is not passed'
#         if len(request.POST.getlist('class_uri')) == 0 and request.POST['class_uris'].strip() == "":
#             error_msg = 'There should be at least one class uri'
#         if error_msg != '':
#             return render(request, 'add_model_abox.html', {'error_msg': error_msg})
#         pid = os.fork()
#         # pid = 1
#         if pid == 0:  # child process
#             print "child is returning"
#             return redirect('list_models')
#         else:  # parent process
#             print "in parent"
#             mlmodel = MLModel()
#             mlmodel.name = clean_string(request.POST['name'])
#             if mlmodel.name.strip() == '':
#                 mlmodel.name = random_string(length=6)
#             mlmodel.url = request.POST['url']
#             mlmodel.extraction_method = MLModel.ABOX
#             mlmodel.save()
#             if request.POST['class_uris'].strip() == "":
#                 class_uris = request.POST.getlist('class_uri')
#             else:
#                 class_uris = []
#                 for cu in request.POST['class_uris'].split(','):
#                     class_uris.append(cu.strip())
#             core.explore_and_train_abox(endpoint=mlmodel.url, model_id=mlmodel.id, min_num_of_objects=30,
#                                         classes_uris=class_uris)
#             os._exit(0)  # to close the thread after finishing
#
#
# def add_model(request):
#     if request.method == 'GET':
#         return render(request, 'add_model.html')
#     elif request.method == 'POST':
#         error_msg = ''
#         if 'url' not in request.POST:
#             error_msg = 'url is not passed'
#         if 'name' not in request.POST:
#             error_msg = 'name is not passed'
#         if error_msg != '':
#             return render(request, 'add_model.html', {'error_msg': error_msg})
#         pid = os.fork()
#         # pid = 1
#         if pid == 0:  # child process
#             print "child is returning"
#             return redirect('list_models')
#         else:  # parent process
#             print "in parent"
#             mlmodel = MLModel()
#             mlmodel.name = clean_string(request.POST['name'])
#             if mlmodel.name.strip() == '':
#                 mlmodel.name = random_string(length=6)
#             mlmodel.url = request.POST['url']
#             mlmodel.extraction_method = MLModel.TBOX
#             mlmodel.save()
#             core.explore_and_train_tbox(endpoint=mlmodel.url, model_id=mlmodel.id)
#             os._exit(0)  # to close the thread after finishing
#
#
# def list_models(request):
#     models = MLModel.objects.all()
#     return render(request, 'list_models.html', {'models': models})
#
#
# def predict(request):
#     if request.method == 'GET':
#         return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE)})
#     else:
#         has_header = False
#         if 'hasheader' in request.POST:
#             has_header = True
#         name = request.POST['name']
#         if name.strip() == '':
#             name = random_string(length=4)
#         model_id = request.POST['model_id']
#         model = MLModel.objects.filter(id=model_id)
#         if len(model) != 1:
#             return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
#                                                     'error_msg': 'this model is not longer exists'})
#         model = model[0]
#         files = request.FILES.getlist('csvfiles')
#         if len(files) == 0:
#             return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
#                                                     'error_msg': 'You should upload csv files to be predicted'})
#         print "name %s num of files %d" % (name, len(files))
#         print "files: "
#         print files
#         stored_files = []
#         original_uploaded_filenames = []
#         for file in files:
#             dest_file_name = name + ' - ' + random_string(length=4) + '.csv'
#             if handle_uploaded_file(uploaded_file=file,
#                                     destination_file=os.path.join(settings.UPLOAD_DIR, dest_file_name)):
#                 stored_files.append(os.path.join(settings.UPLOAD_DIR, dest_file_name))
#                 original_uploaded_filenames.append(file.name)
#         if len(stored_files) == 0:
#             return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
#                                                     'error_msg': 'we could not handle any of the files,' +
#                                                                  ' make sure they are text csv files'})
#         print "stored files:"
#         print stored_files
#         pid = os.fork()
#         # pid = 1
#         if pid == 0:  # child process
#             print "predict> child is returning"
#             return redirect('list_predictionruns')
#         else:  # parent process
#             print "predict> in parent"
#             pr = PredictionRun()
#             pr.mlmodel = model
#             pr.name = name
#             pr.save()
#             if pr.mlmodel.file_name.strip() == '':
#                 for f in stored_files:
#                     os.remove(f)
#                 return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
#                                                         'error_msg': 'The chosen model does not have a model file'})
#             core.predict_files(predictionrun_id=pr.id, model_dir=os.path.join(settings.MODELS_DIR,
#                                                                               pr.mlmodel.file_name),
#                                files=stored_files, has_header=has_header,
#                                original_uploaded_filenames=original_uploaded_filenames)
#             os._exit(0)
#
#
# def list_predictionruns(request):
#     return render(request, 'list_predictions.html', {'predictionruns': PredictionRun.objects.all()})
#
#
# def about(request):
#     return render(request, 'about.html')
#
#
# def handle_uploaded_file(uploaded_file=None, destination_file=None):
#     if uploaded_file is None:
#         print "handle_uploaded_file> uploaded_file should not be None"
#         return False
#     if destination_file is None:
#         print "handle_uploaded_file> destinatino_file should not be None"
#         return False
#     f = uploaded_file
#     with open(destination_file, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     return True
#
#
# def list_memberships(request, predictionrun_id):
#     from django.http import Http404
#     predictionrun = PredictionRun.objects.filter(id=predictionrun_id)
#     if len(predictionrun) != 1:
#         raise Http404("Provided prediction run does not exist")
#     predictionrun = predictionrun[0]
#     mems_and_types = core.get_types_and_membership(top_k_candidates=20, predictionrun_id=predictionrun.id,
#                                                    model_dir=os.path.join(settings.MODELS_DIR,
#                                                                           predictionrun.mlmodel.file_name))
#     print 'mems and types is: '
#     print mems_and_types
#     return render(request, 'list_memberships.html', {'mems_and_types': mems_and_types})
#
#
# #################################################################################
# #                        Online Annotation                                      #
# #################################################################################
#
# class OnlineEntityAnnotation(View):
#     """
#     This to annotate cells with classes and entities
#     :param request:
#     :return:
#     """
#
#     def get(self, request):
#         return render(request, 'online_entity_annotation.html')
#
#     def post(self, request):
#         if 'name' not in request.POST or request.POST['name'].strip() == '':
#             name = random_string(4)
#         else:
#             name = request.POST['name'].strip()
#         files = request.FILES.getlist('csvfiles')
#
#         if len(files) == 0:
#             return render(request, 'online_entity_annotation.html', {'error_msg': 'no csv files are found'})
#         stored_files = []
#         for file in files:
#             dest_file_name = 'annotation' + ' - ' + random_string(length=4) + '.csv'
#             if handle_uploaded_file(uploaded_file=file,
#                                     destination_file=os.path.join(settings.UPLOAD_DIR, dest_file_name)):
#                 sf = os.path.join(settings.UPLOAD_DIR, dest_file_name)
#                 stored_files.append('"' + sf + '"')
#
#         if len(stored_files) == 0:
#             return render(request, 'online_entity_annotation.html', {'error_msg': 'error saving the csv files'})
#         proj_abs_dir = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#         print proj_abs_dir
#         venv_python = os.path.join(proj_abs_dir, '.venv', 'bin', 'python')
#         print venv_python
#         annotation_run = OnlineAnnotationRun(name=name, status="started")
#         annotation_run.save()
#         comm = "%s %s %s --csvfiles %s" % (venv_python,
#                                           (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
#                                           annotation_run.id,
#                                           ",".join(stored_files))
#         print "comm: %s" % comm
#         subprocess.Popen(comm, shell=True)
#         return render(request, 'online_entity_annotation.html', {'msg': 'app is running'})
#
#
# def view_annotation(request):
#     annotation_id = request.GET['annotation'].strip()
#     annotation = OnlineAnnotationRun.objects.get(id=annotation_id)
#     cells = Cell.objects.filter(annotation_run=annotation)
#     return render(request, 'view_annotation.html', {'annotation': annotation, 'cells': cells})
#
#
# def annotation_results(request):
#     annotation_id = request.GET['annotation'].strip()
#     annotation = OnlineAnnotationRun.objects.get(id=annotation_id)
#     return render(request, 'annotation_results.html', {'classes': annotation.results.split(',')})
#
#
# def list_annotations(request):
#     return render(request, 'list_annotations.html', {'annotations': OnlineAnnotationRun.objects.all()})
#
#
# def do_type(request):
#     venv_python = get_python_venv()
#     annotation_id = request.GET['annotation'].strip()
#     comm = "%s %s %s --dotype" % (venv_python,
#                          (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
#                          annotation_id)
#     # commented the below just to try
#     # comm = "%s %s %s --eliminateclasses --omitrootclasses --dotype " % (venv_python,
#     #                      (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
#     #                      annotation_id)
#     print "comm: %s" % comm
#     subprocess.Popen(comm, shell=True)
#     return render(request, 'home.html')
#
#
# def online_annotation_entity_stat(request):
#     ann_run = request.GET['annotation']
#     d = {}
#     annotation_run = OnlineAnnotationRun(id=ann_run)
#     for cell in annotation_run.cells:
#         for entity in cell.entities:
#             for cclass in entity.classes:
#                 if cclass.cclass not in d:
#                     d[cclass.cclass] = []
#                 d[cclass.cclass].append(entity.entity)
#     return render(request, 'view_entity_annotation_stat.html', {'d': d})
#
#
# def advance_annotation(request):
#     if 'ann' not in request.GET or 'alpha' not in request.GET:
#         anns = OnlineAnnotationRun.objects.all()
#         if len(anns) > 0:
#             return render(request, 'advanced_annotation.html', {'anns': anns, 'alpha': 0.3, 'selected': anns[0].id})
#         else:
#             return render(request, 'advanced_annotation.html', {'anns': anns, 'alpha': 0.3, 'selected': 0})
#     else:
#         from annotator import load_graph, score_graph, get_nodes, get_edges
#         alpha = float(request.GET['alpha'])
#         ann_run = OnlineAnnotationRun.objects.get(id=request.GET['ann'])
#         graph = load_graph(ann_run=ann_run)
#         results = score_graph(ann_run=ann_run, alpha=alpha, graph=graph)
#         #graph.draw_with_scores()
#         return render(request, 'advanced_annotation.html',
#                       {'anns': OnlineAnnotationRun.objects.all(), 'alpha': alpha, 'network': 'network',
#                        'highlights': results[:5], 'nodes': get_nodes(graph), 'edges': get_edges(graph),
#                        'results': results, 'selected': ann_run.id})
#
#
# def annotation_stats(request):
#     anns = OnlineAnnotationRun.objects.all()
#     if 'ann' not in request.GET:
#         return render(request, 'annotation_stats.html', {'anns': anns})
#     else:
#         ann = OnlineAnnotationRun.objects.get(id=request.GET['ann'])
#         selected = ann.id
#         # entity linking percentage
#         total_cells = ann.cells
#         ann_cells = [c for c in ann.cells if len(c.entities) > 0]
#         entity_linking = len(ann_cells) * 100.0 / len(total_cells)
#         # average number of entities per cell
#         total_entities = [len(c.entities) for c in ann.cells]
#         print 'total entities'
#         print total_entities
#         entities_per_cell = sum(total_entities) * 1.0 / len(total_cells)
#         entities_per_ann_cell = sum(total_entities) * 1.0 / len(ann_cells)
#         stats = {
#             'entity linking percentage': entity_linking,
#             'average number of entities per cell': entities_per_cell,
#             'average number of entities per annotated cell': entities_per_ann_cell
#         }
#     return render(request, 'annotation_entity_stats.html', {'anns': anns, 'selected': selected, 'stats': stats})
#
#
# def online_annotation_annotation_stat(request):
#     stats = []
#     for o in OnlineAnnotationRun.objects.filter(status='Annotation is complete'):
#         d = {}
#         d["ann"] = o
#         d["entity_linking"] = len([c for c in o.cells if len(c.entities) > 0]) * 100.0 / len(o.cells)
#         d["entities_per_cell"] = sum([len(c.entities) for c in o.cells]) * 1.0 / len(o.cells)
#         ss = [len(c.entities) for c in o.cells if len(c.entities) > 0]
#         d["entities_per_linked_cell"] = sum(ss) * 1.0 / len(ss)
#         # rounding
#         d["entity_linking"] = str(round(d["entity_linking"], 2))
#         d["entities_per_cell"] = str(round(d["entities_per_cell"], 2))
#         d["entities_per_linked_cell"] = str(round(d["entities_per_linked_cell"], 2))
#
#         stats.append(d)
#     return render(request, 'view_annotation_annotation_stat.html', {"stats": stats})
#
#
# def live_monitor(request):
#     statuses = [s.status for s in OnlineAnnotationRun.objects.all()]
#     c = Counter(statuses)
#     return render(request, 'live_monitor.html', {'counters': dict(c)})
#
#
# # Helper Functions
#
#
# def get_python_venv():
#     proj_abs_dir = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
#     venv_python = os.path.join(proj_abs_dir, '.venv', 'bin', 'python')
#     return venv_python
#
#
# def random_string(length=4):
#     return ''.join(random.choice(string.lowercase) for i in range(length))
#
#
# def clean_string(s):
#     return ''.join(e for e in s if e.isalnum() or e == ' ' or e == '_' or e == '-')
#
