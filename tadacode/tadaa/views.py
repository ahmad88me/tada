
import os
import string
import random

from django.shortcuts import render, redirect
from models import MLModel
import core


def home(request):
    # import time
    # pid = os.fork()
    # if pid == 0:
    #     print "child will sleep"
    #     time.sleep(5)
    #     print "child is walking up"
    #     os._exit(0)
    # else:
    #     return render(request, 'home.html')
    return render(request, 'home.html')


def add_model(request):
    if request.method == 'GET':
        return render(request, 'add_model.html')
    elif request.method == 'POST':
        error_msg = ''
        if 'url' not in request.POST:
            error_msg = 'url is not passed'
        if 'name' not in request.POST:
            error_msg = 'name is not passed'
        if error_msg != '':
            return render(request, 'add_model.html', {'error_msg': error_msg})
        pid = os.fork()
        #pid = 1
        if pid == 0:  # child process
            print "child is returning"
            #core.test_progress()
            return redirect('list_models')
            #return render(request, 'add_model.html', {'message': 'model is under processing'})
        else:  # parent process
            print "in parent"
            mlmodel = MLModel()
            mlmodel.name = clean_string(request.POST['name'])
            if mlmodel.name.strip() == '':
                mlmodel.name = random_string(length=6)
            mlmodel.url = request.POST['url']
            mlmodel.save()
            core.explore_and_train(endpoint=mlmodel.url, model_id=mlmodel.id)
            os._exit(0)  # to close the thread after finishing


def list_models(request):
    models = MLModel.objects.all()
    return render(request, 'list_models.html', {'models': models})


def predict(request):
    if request.method == 'GET':
        return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE)})
    else:
        return redirect()


def about(request):
    return render(request, 'about.html')


# Helper Functions


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def clean_string(s):
    return ''.join(e for e in s if e.isalnum() or e == ' ' or e=='_' or e=='-')
