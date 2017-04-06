# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0002_auto_20170406_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionrun',
            name='mlmodel',
            field=models.ForeignKey(default=None, to='tadaa.MLModel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 10, 18, 12, 377197)),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 10, 18, 12, 378149)),
        ),
    ]
