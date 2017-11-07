from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Image, Job

# Create your views here.

# project/deepstyle/
def index(request):
    html = ''

    #querying and templating results from the database
    all_jobs = Job.objects.all()
    template = loader.get_template('deepstyle/index.html')
    context = {
        'all_jobs' : all_jobs,
    }

    return HttpResponse(template.render(context, request))

    # sample html without template
    # for job in all_jobs:
    #     url = '/deepstyle/' + str(job.id)
    #     html += '<a href="' + url + '">' + job.job_name + '</a><br>'
    # return HttpResponse(html)

# project/deepstyle/job_id
def job_detail(request, job_id):
    return HttpResponse('<h1>Job ID: ' + str(job_id) + '</h1>')
