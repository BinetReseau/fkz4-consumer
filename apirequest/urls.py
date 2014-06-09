from django.conf.urls import patterns, url

from apirequest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test/(.*)$', views.request, name='request'),
    url(r'^auth_code_given$', views.auth_code_given, name='auth_code_given'),
)