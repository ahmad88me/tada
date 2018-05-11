#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from collections import Counter

BASE_DIR = '../local_data/'

def get_files_names():
    f = open(os.path.join(BASE_DIR, "web_commons_classes.csv"))
    lines = f.readlines()
    files_names = []
    for line in lines:
        ffname, concept_class = line.strip().split(',')[0], line.strip().split(',')[2]
        fname = ffname.replace('"', '').strip()[:-7]
        files_names.append(fname+".json")
    return files_names


def tables_stats(files_names):
    primary_list = {
        'type': [],
        'orientation': [],
        'entity_column_index': [],
    }
    for fname in files_names:
        f = open(os.path.join(BASE_DIR, "web_commons_tables", fname))
        s = f.read()
        j = json.loads(s)
        primary_list['type'].append(j['tableType'])
        primary_list['orientation'].append(j['tableOrientation'])
        primary_list['entity_column_index'].append(j['keyColumnIndex'])
    stats = {
        'type': dict(Counter(primary_list['type'])),
        'orientation': dict(Counter(primary_list['orientation'])),
        'entity_column_index': dict(Counter(primary_list['entity_column_index']))
    }
    print stats

tables = get_files_names()
tables_stats(tables)