# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tadaa', '0004_auto_20171219_0843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cclass',
            options={'verbose_name_plural': 'CClasses'},
        ),
        migrations.AlterModelOptions(
            name='entity',
            options={'verbose_name_plural': 'Entities'},
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 26, 5, 28, 43, 176000)),
        ),
        migrations.AlterField(
            model_name='predictionrun',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 26, 5, 28, 43, 176918)),
        ),
    ]
