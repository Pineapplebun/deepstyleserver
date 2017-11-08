from django.conf.urls import url
from . import views

app_name = 'deepstyle'

urlpatterns = [
    # url for /deepstyle/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # url for job pages
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # url for adding new job
    url(r'^createjob/$', views.CreateJob.as_view(), name='CreateJob')
]
