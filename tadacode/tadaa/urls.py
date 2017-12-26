from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^add_model_abox', 'tadaa.views.add_model_abox'),
    url(r'^add_model', 'tadaa.views.add_model'),
    url(r'list_models', 'tadaa.views.list_models', name='list_models'),
    url(r'about', 'tadaa.views.about'),
    url(r'^predict', 'tadaa.views.predict', name='predict'),
    url(r'^list_predictions', 'tadaa.views.list_predictionruns', name='list_predictionruns'),
    url(r'list_memberships/([0-9]+)', 'tadaa.views.list_memberships'),
    url(r'get_classes', 'tadaa.views.get_classes'),
    url(r'online_entity_annotation', views.OnlineEntityAnnotation.as_view()),
    url(r'view_annotations', views.view_annotations),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home', 'tadaa.views.home'),
    url('', 'tadaa.views.home'),
)
