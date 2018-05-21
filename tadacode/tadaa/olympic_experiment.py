import chardet
import json
import csv
import os
import sys
import subprocess
from datetime import datetime


#################################################################
#           TO make this app compatible with Django             #
#################################################################

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
venv_python = os.path.join(proj_path, '.venv', 'bin', 'python')
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tadaa.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from tadaa.models import OnlineAnnotationRun
import settings


#############################################################################
#                       Building a date models (pre annotation)             #
#############################################################################

def build_model(annotation_run):
    csv_file_dir = '"'+os.path.join(proj_path, 'explore', 'updated_input_new_for_tada', annotation_run.name)+'"'
    comm = "%s %s %s --csvfiles %s" % (venv_python,
                                       (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                       annotation_run.id,
                                        csv_file_dir)
    print "comm: %s" % comm
    subprocess.call(comm, shell=True)


def build_model_from_id(id):
    run = OnlineAnnotationRun.objects.get(id=id)
    build_model(run)
    print "\n\nModel %s\n\n" % run.name


def build_models():
    runs = OnlineAnnotationRun.objects.filter(status='Ready')
    for r in runs:
        build_model(r)
        print "\n\nModel %s\n\n" % r.name


def build_empty_models():
    files_str = """
    aaaboxers.csv                   
    aaagymnasts.csv                 
    aaaswimmers.csv                 
    aaawrestlers.csv
    aaabadmintonplayers.csv         
    aaacyclists.csv                 
    aaahandballplayers.csv          
    aaatennisplayers.csv
    aaabasketballplayers.csv        
    aaagolfplayers.csv              
    aaarower.csv                    
    aaavolleyballplayers.csv
    """
    lines = files_str.split('\n')
    for line in lines:
        if line.strip() == '':
            continue
        file_name = line.strip()
        annotation_run = OnlineAnnotationRun(name=file_name)
        annotation_run.save()


#########################################
#               Annotation              #
#########################################

def annotate_by_id(id, log=False):
    annotation_run = OnlineAnnotationRun.objects.get(id=id)
    comm = "%s %s %s --dotype" % (venv_python,
                                       (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                       annotation_run.id)
    if log:
        comm += ' >> "%s.log"' % annotation_run.name
    print "comm: %s" % comm
    subprocess.call(comm, shell=True)


def annotate_all():
    runs = OnlineAnnotationRun.objects.filter(status='datasets are added')
    sorted_runs = sorted(runs, key=lambda r: len(r.cells))
    for r in sorted_runs:
        print "%s annotating %s" % (str(datetime.now()), r.name)
        annotate_by_id(r.id, log=True)

#build_empty_models()
#build_models()
annotate_all()