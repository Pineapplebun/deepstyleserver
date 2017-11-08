from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Job

class IndexView(generic.ListView):
    template_name = 'deepstyle/index.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Job.objects.all()

class DetailView(generic.DetailView):
    model = Job
    template_name = 'deepstyle/detail.html'

class CreateJob(CreateView):
    model = Job
    fields = ['job_name', 'job_description', 'input_image', 'output_width', 'content_weight', 'pooling']

class EditJob(UpdateView):
    model = Job
    fields = ['job_name', 'job_description']

class DeleteJob(DeleteView):
    model = Job
    success_url = reverse_lazy('deepstyle:index')
