# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(default=b'', max_length=120)),
                ('column_no', models.PositiveIntegerField()),
                ('values', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=120)),
                ('file_name', models.CharField(default=b'', max_length=80)),
                ('url', models.URLField()),
                ('public', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2017, 4, 6, 9, 40, 31, 888374))),
                ('progress', models.PositiveIntegerField(default=0)),
                ('notes', models.CharField(max_length=120)),
                ('state', models.CharField(default=b'notstarted', max_length=10, choices=[(b'running', b'Running'), (b'stopped', b'Stopped'), (b'complete', b'Complete'), (b'notstarted', b'Not Started Yet')])),
                ('owner', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PredictionRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=120)),
                ('types', models.TextField(default=b'')),
                ('created_on', models.DateTimeField(default=datetime.datetime(2017, 4, 6, 9, 40, 31, 889372))),
                ('progress', models.PositiveIntegerField(default=0)),
                ('notes', models.CharField(max_length=120)),
                ('state', models.CharField(default=b'notstarted', max_length=10, choices=[(b'running', b'Running'), (b'stopped', b'Stopped'), (b'complete', b'Complete'), (b'notstarted', b'Not Started Yet')])),
                ('owner', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='prediction_run',
            field=models.ForeignKey(to='tadaa.PredictionRun'),
            preserve_default=True,
        ),
    ]
