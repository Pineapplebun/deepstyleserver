from django.views import generic
from .models import Job

class IndexView(generic.ListView):
    template_name = 'deepstyle/index.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Job.objects.all()

class DetailView(generic.DetailView):
    model = Job
    template_name = 'deepstyle/detail.html'
