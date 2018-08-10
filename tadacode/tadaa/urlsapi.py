from django.conf.urls import url
import viewsapi as views

urlpatterns = [
    url(r'type_entity_col', views.type_entity_col),
    url(r'get_col_type', views.get_col_type),
    url(r'webcommons_get_col_type', views.webcommons_get_col_type),
]
