import os
import string
import random
from collections import Counter

import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
import core
from django.views.generic import View
import subprocess
from django.views.decorators.csrf import csrf_exempt

from views import handle_uploaded_file, random_string
import viewscommons

@csrf_exempt
def type_entity_col(request):
    if request.method == "post":
        if 'name' not in request.POST or request.POST['name'].strip() == '':
            name = random_string(4)
        else:
            name = request.POST['name'].strip()

        files = request.FILES.getlist('csvfiles')
        error_msg = viewscommons.store_uploaded_csv_files(files)

        if error_msg != "":
            return JsonResponse({'error': error_msg}, status=400)


        viewscommons.build_entity_model(name, files)
        JsonResponse({'msg': ''})
        return render(request, 'online_entity_annotation.html', {'msg': 'app is running'})
    else:
        return JsonResponse({'error': 'Only POST is supported'}, status=405)




