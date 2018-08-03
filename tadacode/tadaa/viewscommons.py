from models import AnnRun, EntityAnn
import os
import settings
import random
import string
import subprocess
import logging
from settings import LOG_ABS_DIR

from logger import set_config


logger = set_config(logging.getLogger(__name__), logdir=os.path.join(LOG_ABS_DIR, 'tada.log'))


def store_uploaded_csv_files(csv_files):
    """
    :param csv_files: list of files uploaded (request.FILES.getlist)
    :return: empty string if success, otherwise will return the error msg and also a list of stored files
    """
    if len(csv_files) == 0:
        error_msg = "no csv files are found"
        logger.error(error_msg)
        return error_msg, []
    stored_files = []
    for file in csv_files:
        dest_file_name = 'annotation' + ' - ' + random_string(length=4) + '.csv'
        if handle_uploaded_file(uploaded_file=file,
                                destination_file=os.path.join(settings.UPLOAD_DIR, dest_file_name)):
            sf = os.path.join(settings.UPLOAD_DIR, dest_file_name)
            stored_files.append('"' + sf + '"')
    if len(stored_files) == 0:
        error_msg = "error saving the csv files"
        logger.error(error_msg)
        return error_msg, []
    return "", stored_files


def handle_uploaded_file(uploaded_file=None, destination_file=None):
    if uploaded_file is None:
        logger.error("uploaded_file should not be None")
        return False
    if destination_file is None:
        logger.error("destination_file should not be None")
        return False
    f = uploaded_file
    with open(destination_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True


def random_string(length=4):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def create_and_type_entity_column(name, files):
    proj_abs_dir = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    logger.debug(proj_abs_dir)
    venv_python = os.path.join(proj_abs_dir, '.venv', 'bin', 'python')
    logger.debug(venv_python)
    ann_run = AnnRun(name=name, status="started")
    ann_run.save()
    comm = "%s %s %s --onlyprefix %s --dotype --csvfiles %s" % (venv_python,
                                       (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'annotator.py')),
                                       ann_run.id,
                                       "http://dbpedia.org/ontology",
                                       ",".join(files))
    logger.debug("comm: %s" % comm)
    subprocess.Popen(comm, shell=True)
    return ann_run