
import os
import string
import random

import settings
from django.shortcuts import render, redirect
from models import MLModel, PredictionRun
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
        name = request.POST['name']
        if name.strip() == '':
            name = random_string(length=4)
        model_id = request.POST['model_id']
        model = MLModel.objects.filter(id=model_id)
        if len(model) != 1:
            return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
                                                    'error_msg': 'this model is not longer exists'})
        model = model[0]
        files = request.FILES.getlist('csvfiles')
        if len(files) == 0:
            return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
                                                    'error_msg': 'You should upload csv files to be predicted'})
        print "name %s num of files %d" % (name, len(files))
        print "files: "
        print files
        # name = name + ' - ' + random_string(length=4) + '.csv'
        stored_files = []
        for file in files:
            dest_file_name = name + ' - ' + random_string(length=4) + '.csv'
            if handle_uploaded_file(uploaded_file=file, destination_file=os.path.join(settings.UPLOAD_DIR, dest_file_name)):
                stored_files.append(os.path.join(settings.UPLOAD_DIR, dest_file_name))
        if len(stored_files) == 0:
            return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
                                                    'error_msg': 'we could not handle any of the files,' +
                                                                 ' make sure they are text csv files'})
        print "stored files:"
        print stored_files
        #pid = os.fork()
        pid = 1
        if pid == 0:  # child process
            print "predict> child is returning"
            return redirect('list_predictionruns')
        else:  # parent process
            print "predict> in parent"
            pr = PredictionRun()
            pr.mlmodel = model
            pr.name = name
            pr.save()
            if pr.mlmodel.file_name.strip() == '':
                for f in stored_files:
                    os.remove(f)
                return render(request, 'predict.html', {'models': MLModel.objects.filter(state=MLModel.COMPLETE),
                                                        'error_msg': 'The chosen model does not have a model file'})
            # print "pr.mlmodel.file_name> "+pr.mlmodel.file_name
            # print "full> "+os.path.join(settings.MODELS_DIR, pr.mlmodel.file_name)
            core.predict_files(predictionrun_id=pr.id, model_dir=os.path.join(settings.MODELS_DIR,pr.mlmodel.file_name),
                               files=stored_files)
            os._exit(0)
            # return redirect('list_predictionruns')


def list_predictionruns(request):
    return render(request, 'list_predictions.html', {'predictionruns': PredictionRun.objects.all()})


def about(request):
    return render(request, 'about.html')


def handle_uploaded_file(uploaded_file=None, destination_file=None):
    if uploaded_file is None:
        print "handle_uploaded_file> uploaded_file should not be None"
        return False
    if destination_file is None:
        print "handle_uploaded_file> destinatino_file should not be None"
        return False
    f = uploaded_file
    with open(destination_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True


# Helper Functions


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def clean_string(s):
    return ''.join(e for e in s if e.isalnum() or e == ' ' or e=='_' or e=='-')
