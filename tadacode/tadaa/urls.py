from django.conf.urls import url, include
from django.contrib import admin
import views
import urlsapi

urlpatterns = [
    # url(r'^add_model_abox', 'tadaa.views.add_model_abox'),
    # url(r'^add_model', 'tadaa.views.add_model'),
    # url(r'^list_models', 'tadaa.views.list_models', name='list_models'),
    # url(r'^about', 'tadaa.views.about'),
    # url(r'^predict', 'tadaa.views.predict', name='predict'),
    # url(r'^list_predictions', 'tadaa.views.list_predictionruns', name='list_predictionruns'),
    # url(r'^list_memberships/([0-9]+)', 'tadaa.views.list_memberships'),
    # url(r'^get_classes', 'tadaa.views.get_classes'),
    # url(r'^online_entity_annotation', views.OnlineEntityAnnotation.as_view()),
    # url(r'^view_classes_stat', views.online_annotation_entity_stat),
    # url(r'^view_annotation_stat', views.online_annotation_annotation_stat),
    # url(r'^view_annotation', views.view_annotation),
    # url(r'^list_annotations', views.list_annotations),
    # url(r'^annotation_results', views.annotation_results),
    # url(r'^advanced_annotation', views.advance_annotation),
    # url(r'^do_type', views.do_type),
    # url(r'^annotation_stats', views.annotation_stats),
    # url(r'live_monitor', views.live_monitor),
    url(r'^admin/', include(admin.site.urls)),
    url(r'e_ann_list', views.e_ann_list),
    url(r'entity_ann_raw_results', views.entity_ann_raw_results),
    url(r'entity_ann_results', views.entity_ann_results),
    url(r'entity_ann_recompute', views.entity_ann_recompute),
    url(r'^api/', include(urlsapi)),
    url(r'', views.home),
    #url('', 'tadaa.views.home'),
]


