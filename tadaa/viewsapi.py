from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import viewscommons
from models import EntityAnn, AnnRun


@csrf_exempt
def type_entity_col(request):
    """
    post values:
        name: (Optional) The name of the annotation run
        csv_file: The content of the CSV file (not the URL)
        entity_col_id: (Optional) The id of the entity column, 0 if not provided
    :param request:
    :return:
    """
    entity_col_id = 0
    if request.method == "POST":
        if 'name' not in request.POST or request.POST['name'].strip() == '':
            name = viewscommons.random_string(4)
        else:
            name = request.POST['name'].strip()
        anns = AnnRun.objects.filter(name=name)
        if len(anns) != 0:  # the name already taken
            return JsonResponse({'error': 'the name is already exists, please choose another one'}, status=400)
        files = request.FILES.getlist('csv_file')
        if len(files) > 0:
            error_msg, stored_files = viewscommons.store_uploaded_csv_files(files)
        else:
            error_msg, stored_files = viewscommons.store_url_csv_files(request.POST['csv_url'])
        if error_msg != "":
            return JsonResponse({'error': error_msg}, status=400)
        if 'entity_col_id' in request.POST:
            try:
                entity_col_id = int(request.POST['entity_col_id'])
            except Exception as e:
                return JsonResponse({'error': 'entity_col_id should be an integer'})
        ann_run = viewscommons.create_and_type_entity_column(name, stored_files, entity_col_id=entity_col_id)
        return JsonResponse({'id': str(ann_run.id), 'name': ann_run.name, 'msg': 'The entity column is being annotated'})
        #return render(request, 'online_entity_annotation.html', {'msg': 'app is running'})
    else:
        return JsonResponse({'error': 'Only POST is supported'}, status=405)


def get_col_type(request):
    MAX_K = 5
    if request.method != "GET":
        return JsonResponse({'error': 'This endpoint only accepts GET'}, status=405)
    else:
        alpha = 0.1
        k = 1
        if 'id' not in request.GET and 'name' not in request.GET:
            return JsonResponse({'error': 'annotation run id or name should be passed'}, status=400)
        if 'alpha' in request.GET:
            try:
                alpha = float(request.GET['alpha'])
            except:
                return JsonResponse({'error': 'alpha should be between 0 and 1'}, status=400)
            if alpha > 1 or alpha < 0:
                return JsonResponse({'error': 'alpha should be between 0 and 1'}, status=400)
        if 'k' in request.GET:
            if not request.GET['k'].isdigit():
                return JsonResponse({'error': 'k should be an integer between 1 and %d'% MAX_K}, status=400)
            k = int(request.GET['k'])
            if k > MAX_K or k < 1:
                return JsonResponse({'error': 'k should be an integer between 1 and %d'% MAX_K}, status=400)

        from annotator import load_graph, score_graph, get_nodes, get_edges
        if 'id' in request.GET:
            anns = AnnRun.objects.filter(id=request.GET['id'])
        else:
            anns = AnnRun.objects.filter(name=request.GET['name'])
        if len(anns) != 1:
            return JsonResponse({'error': 'incorrect annotation run id'}, status=400)
        ann_run = anns[0]
        if len(ann_run.entityann_set.all()) != 1:
            return JsonResponse({'error': 'this annotation does not have any annotation results'}, status=500)

        entity_ann = ann_run.entityann_set.all()[0]
        graph = load_graph(entity_ann=entity_ann)
        results = score_graph(entity_ann=entity_ann, alpha=alpha, graph=graph)
        return JsonResponse({'results': results[:k], 'alpha': alpha, 'k': k})


def webcommons_get_col_type(request):
    if 'file_name' in request.GET:
        # ann_run = AnnRun.objects.get(name__contains=request.GET['file_name'])
        ann_run = AnnRun.objects.get(name__startswith=request.GET['file_name'])
        #eann = ann_run.entityann_set.all()[0]
        request.GET = request.GET.copy()
        request.GET['id'] = str(ann_run.id)
        return get_col_type(request)
    else:
        return JsonResponse({'error': 'file_name is not passed'}, status=400)


def check_status(request):
    """
    This is mainly for AINNotation
    :param request:
    :return:
    """
    if 'name' in request.GET:
        name = request.GET['name']
        anns = AnnRun.objects.filter(name=name)
        if len(anns) == 1:
            ann = anns[0]
            if ann.status == 'Annotation is complete':
                status = 'Annotated'
            else:
                status = 'In progress'
        elif len(anns) == 0:
            status = 'Not enabled'
        else:
            status = 'Multiple runs with the same name'
        return JsonResponse({'status': status})
    else:
        return JsonResponse({'error': 'name is not passed'})