from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from .models import Job

class LoginRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated, login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'deepstyle/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_jobs'] = Job.objects.all()
        context['jobs_in_progress'] = Job.objects.filter(job_status='P')
        context['jobs_in_queue'] = Job.objects.filter(job_status='Q')
        context['jobs_completed'] = Job.objects.filter(job_status='C')
        context['jobs_failed'] = Job.objects.filter(Q(job_status='F') | Q(job_status='PF'))
        return context

    def get_queryset(self):
        return

class GalleryView(LoginRequiredMixin, generic.ListView):
    template_name = 'deepstyle/gallery.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        return Job.objects.all()

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'deepstyle/detail.html'

class CreateJob(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['job_name', 'job_description', 'input_image', 'style_image', 'output_width', 'iterations', 'content_weight', 'content_weight_blend', 'style_weight', 'style_scale', 'style_blend_weights', 'learning_rate', 'style_layer_weight_exp', 'preserve_color', 'pooling']

class EditJob(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['job_name', 'job_description']

class DeleteJob(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('deepstyle:index')
