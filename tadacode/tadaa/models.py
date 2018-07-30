import os
import numpy as np

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from settings import MODELS_DIR


class AnnRun(models.Model):
    name = models.CharField(max_length=120, default='')
    status = models.CharField(max_length=120, default='Ready')
    datetime = datetime.now


class EntityAnn(models.Model):
    ann_run = models.ForeignKey(AnnRun)
    results = models.CharField(max_length=500, default='')
    graph_file = models.FileField(upload_to=MODELS_DIR, default=os.path.join(MODELS_DIR, 'default.graph'))

    @property
    def cells(self):
        return Cell.objects.filter(annotation_run=self)

    def __str__(self):
        return str(self.id) + '> ' + self.ann_run.name + "(" + self.status + ")"


class Cell(models.Model):
    annotation_run = models.ForeignKey(EntityAnn)
    text_value = models.TextField()

    @property
    def entities(self):
        return Entity.objects.filter(cell=self)

    def __str__(self):
        return self.annotation_run.name + ' - ' + self.text_value


class Entity(models.Model):
    cell = models.ForeignKey(Cell)
    entity = models.CharField(max_length=250)

    @property
    def classes(self):
        return CClass.objects.filter(entity=self)

    class Meta:
        verbose_name_plural = "Entities"

    def __str__(self):
        return self.cell.text_value + ' - ' + self.entity


class CClass(models.Model):
    entity = models.ForeignKey(Entity)
    cclass = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "CClasses"

    def __str__(self):
        return self.entity.entity + ' - ' + self.cclass
