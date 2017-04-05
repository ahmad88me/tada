from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class MLModel(models.Model):
    name = models.CharField(max_length=120, default='')
    file_name = models.CharField(max_length=80, default='')
    url = models.URLField()
    public = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=datetime.now())
    owner = models.OneToOneField(User, null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=120)

    NOT_STARTED = 'notstarted'
    RUNNING = 'running'
    STOPPED = 'stopped'
    COMPLETE = 'complete'
    STATE_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped'),
        (COMPLETE, 'Complete'),
        (NOT_STARTED, 'Not Started Yet')
    )
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=NOT_STARTED)

    def __unicode__(self):
        return self.name


# class PredictionRun(models.Model):
#     name = models.CharField(max_length=120, default='')
#     #files = models.CharField(max_length=500, default='')
#     url = models.URLField()
#     public = models.BooleanField(default=True)
#     created_on = models.DateTimeField(default=datetime.now())
#     owner = models.OneToOneField(User, null=True, blank=True)
#     progress = models.PositiveIntegerField(default=0)
#     notes = models.CharField(max_length=120)
#     NOT_STARTED = 'notstarted'
#     RUNNING = 'running'
#     STOPPED = 'stopped'
#     COMPLETE = 'complete'
#     STATE_CHOICES = (
#         (RUNNING, 'Running'),
#         (STOPPED, 'Stopped'),
#         (COMPLETE, 'Complete'),
#         (NOT_STARTED, 'Not Started Yet')
#     )
#     state = models.CharField(max_length=10, choices=STATE_CHOICES, default=NOT_STARTED)
#
#     # def get_files(self):
#     #     return self.files.split(',')
#     #
#     # def set_files(self, files):
#     #     self.files = ','.join(files)
#     #     return self
#
#     def __unicode__(self):
#         return self.name
#
#
# class Membership(models.Model):
#     file_name = models.CharField(max_length=120, default='')
#     column_no = models.PositiveIntegerField()
#     prediction_run = models.ManyToOneRel(PredictionRun)
#
