from tadaa.models import OnlineAnnotationRun, EntityClassCombination, TextEntry

def annotate_csvs(files):
    """
    :param files: a list of files in abs dir
    :return: Nothing
    """
    for f in files:
        annotate_single_csv(f)


def annotate_single_csv(csv_file):
    pass
