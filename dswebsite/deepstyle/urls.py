from django.conf.urls import url
from . import views

app_name = 'deepstyle'

urlpatterns = [
    # url for /deepstyle/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # url for job gallery
    url(r'^gallery/$', views.GalleryView.as_view(), name='gallery'),

    # url for job pages
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # url for adding new job
    url(r'^createjob/$', views.CreateJob.as_view(), name='CreateJob'),

    # url for editing a job
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditJob.as_view(), name='EditJob'),

    # url for deleting a job
    url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteJob.as_view(), name='DeleteJob'),

]
