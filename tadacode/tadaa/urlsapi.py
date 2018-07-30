from django.conf.urls import patterns, include, url
from django.contrib import admin
import viewsapi as views
from django.conf import settings

urlpatterns = patterns('',
                       url(r'type_entity_col', views.type_entity_col),
                       )
