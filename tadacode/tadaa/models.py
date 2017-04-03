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



