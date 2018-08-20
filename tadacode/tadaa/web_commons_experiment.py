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

from tadaa.models import AnnRun
import settings
from settings import LOG_DIR

#################################################################################
#                           JSON to CSV                                         #
#################################################################################
import sys
import logging
from logger import set_config
logger = set_config(logging.getLogger(__name__), logdir=os.path.join(LOG_DIR, 'tada_v1.log'))


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
#                          Test the web commons v2
######################################################################################


def build_empty_models_from_status():
    f = open("local_data/status.csv")
    lines = f.readlines()
    for line in lines:
        file_name = line.strip()
        if len(AnnRun.objects.filter(name=file_name)) == 0:
            annotation_run = AnnRun(name=file_name, status='Created')
            annotation_run.save()


def annotate_models():
    anns = AnnRun.objects.filter(status='Created')
    for ann_run in anns:
        ann_run.status="started"
        ann_run.save()
        csv_file_dir = '"'+os.path.join(proj_path, settings.UPLOAD_DIR, ann_run.name)+'"'
        comm = "%s %s %s --onlyprefix %s --dotype --logdir %s --csvfiles %s" % (venv_python,
                                           (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                           str(ann_run.id),
                                           "http://dbpedia.org/ontology",
                                            os.path.join(LOG_DIR, str(ann_run.id)+'.log'),
                                           csv_file_dir)
        logger.debug("comm: %s" % comm)
        subprocess.call(comm, shell=True)
        #return ann_run


def workflow():
    build_empty_models_from_status()
    annotate_models()


#workflow()

######################################################################################
#                          Test the web commons v1
######################################################################################


def build_empty_models_v1(file_dir):
    import pandas as pd
    df = pd.read_csv(file_dir, header=None)
    for index, row in df.iterrows():
        file_name = 'v1_'+row[0]
        if len(AnnRun.objects.filter(name=file_name)) == 0:
            annotation_run = AnnRun(name=file_name, status='Created')
            annotation_run.save()


def annotate_models_v1(data_folder):
    anns = AnnRun.objects.filter(status='Created')
    for ann_run in anns:
        ann_run.status="started"
        ann_run.save()
        csv_file_dir = '"'+os.path.join(data_folder, ann_run.name[3:])+'"'
        comm = "%s %s %s --onlyprefix %s --dotype --logdir %s --csvfiles %s" % (venv_python,
                                           (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                           str(ann_run.id),
                                           "http://dbpedia.org/ontology",
                                            os.path.join(LOG_DIR, str(ann_run.id)+'.log'),
                                           csv_file_dir)
        logger.debug("comm: %s" % comm)
        subprocess.call(comm, shell=True)
        #return ann_run


def workflow_v1(file_dir, data_folder):
    build_empty_models_v1(file_dir)
    annotate_models_v1(data_folder)


file_dir = sys.argv[1]
data_folder = sys.argv[2]
workflow_v1(file_dir, data_folder)
