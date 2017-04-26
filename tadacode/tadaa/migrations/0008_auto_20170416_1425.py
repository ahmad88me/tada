# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0007_auto_20170406_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodel',
            name='extraction_method',
            field=models.CharField(default=b'tbox', max_length=10, choices=[(b'tbox', b'T-Box'), (b'abox', b'A-Box')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 16, 14, 25, 2, 112168)),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 16, 14, 25, 2, 113149)),
        ),
    ]
