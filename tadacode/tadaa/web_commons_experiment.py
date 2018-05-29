import chardet
import json
import csv
import os
import sys
import subprocess
from datetime import datetime
# f = open("web_commons_progress.txt")


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


#################################################################################
#                           JSON to CSV                                         #
#################################################################################


def web_commons_json_table_to_csv(in_file_dir, out_file_dir):
    fin = open(in_file_dir)
    s_raw = fin.read()
    detected_encoding = chardet.detect(s_raw)
    s = s_raw.decode(detected_encoding['encoding'])
    j = json.loads(s)
    index = j["keyColumnIndex"]
    entity_column = j["relation"][index]
    entities = []
    for e in entity_column:
        ee = e.replace('"', '').strip()
        ee = '"'+ee+'"'
        entities.append(ee)
    fout = open(out_file_dir, 'w')
    fout.write(("\n".join(entities)).encode('utf8'))
    fout.close()


# inp = "local_data/web_commons_tables/1438042986423_95_20150728002306-00329-ip-10-236-191-2_805336391_10.json"
# outp = "local_uploads/1438042986423_95_20150728002306-00329-ip-10-236-191-2_805336391_10.csv"
# web_commons_json_to_csv(inp,outp)


def web_commons_to_csv():
    f = open("local_data/web_commons_classes.csv")
    reader = csv.reader(f)
    for line in reader:
        file_name = line[0][:-7]
        concept = line[1].replace(' ', '_')
        print file_name, concept
        output_file = "local_uploads/web_commons_%s_%s.csv" % (concept, file_name)
        input_file = "local_data/web_commons_tables/%s.json" % file_name
        web_commons_json_table_to_csv(input_file, output_file)


def build_status_file():
    f = open("local_data/web_commons_classes.csv")
    reader = csv.reader(f)
    files = []
    for line in reader:
        file_name = line[0][:-7]
        concept = line[1].replace(' ', '_')
        print file_name, concept
        file_name = "web_commons_%s_%s.csv" % (concept, file_name)
        files.append(file_name)
    f = open("local_data/status.csv", 'w')
    for ff in files:
        f.write('%s\n' % ff)
    f.close()

#build_status_file()
#web_commons_to_csv()

######################################################################################
#                          Test the web commons
######################################################################################


def build_model(annotation_run):
    csv_file_dir = '"'+os.path.join(proj_path, settings.UPLOAD_DIR, annotation_run.name)+'"'
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


def build_empty_models_from_status():
    f = open("local_data/status.csv")
    lines = f.readlines()
    for line in lines:
        file_name = line.strip()
        annotation_run = OnlineAnnotationRun(name=file_name)
        annotation_run.save()


def annotate_by_id(id, log=False):
    annotation_run = OnlineAnnotationRun.objects.get(id=id)
    comm = "%s %s %s --dotype" % (venv_python,
                                       (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                       annotation_run.id)
    if log:
        comm += ' >> %d.log' % annotation_run.id
    print "comm: %s" % comm
    subprocess.call(comm, shell=True)


def build_model_from_id(id):
    run = OnlineAnnotationRun.objects.get(id=id)
    build_model(run)
    print "\n\nModel %s\n\n" % run.name


def annotate_all():
    runs = OnlineAnnotationRun.objects.filter(status='datasets are added')
    # added reverse for the server run
    sorted_runs = sorted(runs, key=lambda r: len(r.cells), reverse=True)
    for r in sorted_runs:
        print "%s annotating %s" % (str(datetime.now()), r.name)
        annotate_by_id(r.id, log=True)


# to create empty models (done) step 1
#build_empty_models_from_status()
# to annotate models (in progress) step 2
build_models()
# testing
#print sys.argv
#build_model_from_id(sys.argv[1])
#build_model_from_id(712)
# annotate_by_id(596)
#annotate_by_id(sys.argv[1])
# step 4
#annotate_all()