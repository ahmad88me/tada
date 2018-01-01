from django.contrib import admin
from tadaa.models import MLModel, PredictionRun, Membership, OnlineAnnotationRun, Cell, Entity, CClass

admin.site.register(MLModel)
admin.site.register(PredictionRun)
admin.site.register(Membership)
admin.site.register(CClass)
admin.site.register(Entity)
admin.site.register(Cell)
admin.site.register(OnlineAnnotationRun)
