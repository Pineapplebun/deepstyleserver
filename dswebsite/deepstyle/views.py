from django.shortcuts import render
from django.http import Http404
from .models import Image, Job

# Create your views here.

# project/deepstyle/
def index(request):
    html = ''

    #querying and templating results from the database
    all_jobs = Job.objects.all()
    for job in all_jobs:
        print (job.job_name)
        
    context = {
        'all_jobs' : all_jobs,
    }

    return render(request, 'deepstyle/index.html', context)

# project/deepstyle/job_id
def job_details(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("A job with ID " + job_id + " does not exist")

    context = {
        'job' : job,
    }

    return render(request, 'deepstyle/job_details.html', context)
