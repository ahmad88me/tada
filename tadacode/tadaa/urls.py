from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tadaa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^add_model', 'tadaa.views.add_model'),
    url(r'list_models', 'tadaa.views.list_models', name='list_models'),
    url(r'^home', 'tadaa.views.home'),

    url(r'^admin/', include(admin.site.urls)),
)
