from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url for job pages
    url(r'^(?P<job_id>[0-9]+)/$', views.job_detail, name='job_detail'),
]
