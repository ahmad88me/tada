# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionrun',
            name='public',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 9, 40, 52, 64528)),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 6, 9, 40, 52, 65427)),
        ),
    ]
