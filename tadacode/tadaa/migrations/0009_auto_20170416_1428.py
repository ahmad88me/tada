# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0008_auto_20170416_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 16, 14, 28, 0, 256028)),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='extraction_method',
            field=models.CharField(max_length=10, choices=[(b'tbox', b'T-Box'), (b'abox', b'A-Box')]),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 16, 14, 28, 0, 257027)),
        ),
    ]
