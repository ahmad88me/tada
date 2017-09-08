from django.contrib import admin
from tadaa.models import MLModel, PredictionRun, Membership, OnlineAnnotationRun, EntityClassCombination, TextEntry

admin.site.register(MLModel)
admin.site.register(PredictionRun)
admin.site.register(Membership)
admin.site.register(EntityClassCombination)
admin.site.register(TextEntry)
admin.site.register(OnlineAnnotationRun)
