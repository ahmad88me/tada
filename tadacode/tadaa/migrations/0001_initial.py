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
            name='CClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cclass', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'CClasses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_value', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(max_length=250)),
                ('cell', models.ForeignKey(to='tadaa.Cell')),
            ],
            options={
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model,),
        ),
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
                ('created_on', models.DateTimeField(default=datetime.datetime(2018, 2, 15, 16, 5, 27, 751290))),
                ('progress', models.PositiveIntegerField(default=0)),
                ('notes', models.CharField(max_length=120)),
                ('extraction_method', models.CharField(max_length=10, choices=[(b'tbox', b'T-Box'), (b'abox', b'A-Box')])),
                ('state', models.CharField(default=b'notstarted', max_length=10, choices=[(b'running', b'Running'), (b'stopped', b'Stopped'), (b'complete', b'Complete'), (b'notstarted', b'Not Started Yet')])),
                ('owner', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OnlineAnnotationRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=120)),
                ('status', models.CharField(default=b'Ready', max_length=120)),
                ('results', models.CharField(default=b'', max_length=500)),
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
                ('public', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2018, 2, 15, 16, 5, 27, 752149))),
                ('progress', models.PositiveIntegerField(default=0)),
                ('notes', models.CharField(max_length=120)),
                ('state', models.CharField(default=b'notstarted', max_length=10, choices=[(b'running', b'Running'), (b'stopped', b'Stopped'), (b'complete', b'Complete'), (b'notstarted', b'Not Started Yet')])),
                ('mlmodel', models.ForeignKey(to='tadaa.MLModel')),
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
        migrations.AddField(
            model_name='cell',
            name='annotation_run',
            field=models.ForeignKey(to='tadaa.OnlineAnnotationRun'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cclass',
            name='entity',
            field=models.ForeignKey(to='tadaa.Entity'),
            preserve_default=True,
        ),
    ]
