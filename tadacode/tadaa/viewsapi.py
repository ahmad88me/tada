from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import viewscommons
from models import EntityAnn, AnnRun


@csrf_exempt
def type_entity_col(request):
    if request.method == "POST":
        if 'name' not in request.POST or request.POST['name'].strip() == '':
            name = viewscommons.random_string(4)
        else:
            name = request.POST['name'].strip()

        files = request.FILES.getlist('csv_file')
        error_msg, stored_files = viewscommons.store_uploaded_csv_files(files)

        if error_msg != "":
            return JsonResponse({'error': error_msg}, status=400)
        ann_run = viewscommons.create_and_type_entity_column(name, stored_files)
        JsonResponse({'id': str(ann_run.id), 'name': ann_run.name, 'msg': 'The entity column is being annotated'})
        return render(request, 'online_entity_annotation.html', {'msg': 'app is running'})
    else:
        return JsonResponse({'error': 'Only POST is supported'}, status=405)


def get_col_type(request):
    MAX_K = 5
    if request.method != "GET":
        return JsonResponse({'error': 'This endpoint only accepts GET'}, status=405)
    else:
        alpha = 0.1
        k = 1
        if 'id' not in request.GET:
            return JsonResponse({'error': 'annotation run id should be passed'}, status=400)
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
        anns = AnnRun.objects.filter(id=request.GET['id'])
        if len(anns) != 1:
            return JsonResponse({'error': 'incorrect annotation run id'}, status=400)
        ann_run = anns[0]
        if len(ann_run.entityann_set.all()) != 1:
            return JsonResponse({'error': 'this annotation does not have any annotation results'}, status=500)

        entity_ann = ann_run.entityann_set.all()[0]
        graph = load_graph(entity_ann=entity_ann)
        results = score_graph(entity_ann=entity_ann, alpha=alpha, graph=graph)
        return JsonResponse({'results': results[:k], 'alpha': alpha, 'k': k})
