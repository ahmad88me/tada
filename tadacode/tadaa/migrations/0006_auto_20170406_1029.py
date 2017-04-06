# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0005_auto_20170406_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 10, 29, 15, 766195)),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 10, 29, 15, 767215)),
        ),
    ]
