import os, sys

proj_path = ((os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tadaa.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from tadaa.models import OnlineAnnotationRun, Cell, CClass, Entity

import sys

def annotate_csvs(files):
    """
    :param files: a list of files in abs dir
    :return: Nothing
    """
    for f in files:
        annotate_single_csv(f)


def annotate_single_csv(csv_file):
    print 'annotating: '+csv_file


if __name__ == '__main__':
    files = sys.argv[1:]
    annotate_csvs(files)