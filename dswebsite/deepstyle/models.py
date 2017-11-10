from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse

# Image model for holding the image
class Image(models.Model):
    image_name = models.CharField(max_length = 500)
    image_description = models.TextField(default = "Just another image")
    image_file = models.ImageField()

    # image type
    INPUT_IMAGE = 'I'
    OUTPUT_IMAGE = 'O'
    IMAGE_TYPE_OPTIONS = (
        (INPUT_IMAGE, "Input"),
        (OUTPUT_IMAGE, "Output")
    )
    image_type = models.CharField(max_length = 1, choices = IMAGE_TYPE_OPTIONS, default = INPUT_IMAGE)

    # string repr. of the class
    def __str__(self):
        return self.image_name


# Job model using image from
class Job(models.Model):
    # basic inputs for the job
    job_name = models.CharField(max_length = 200)
    job_description = models.TextField(default="Just another deepstyle job")

    input_image = models.ForeignKey(Image, blank = False, null = "False", related_name='+')
    style_image = models.ForeignKey(Image, blank = False, null = "False",  related_name='+')
    output_image = models.CharField(max_length = 100, blank = True, null = True)

    # parameters for running a job
    # TOFIX: add more restricted limit to each param?
    output_width = models.PositiveSmallIntegerField()
    iterations = models.PositiveIntegerField(default = 1000)
    content_weight = models.FloatField(default = 5e0)
    content_weight_blend = models.FloatField(default = 1)
    style_weight = models.FloatField(default = 5e2)
    style_scale = models.FloatField(default = 1.0)
    learning_rate = models.FloatField(default = 1e1)
    style_layer_weight_exp = models.FloatField(default = 1)
    perserve_color = models.BooleanField(default = False)

    # pooling
    POOLING_OPTIONS = (
        ('MAX', "max"),
        ('AVG', "avg")
    )
    pooling = models.CharField(max_length = 3, choices = POOLING_OPTIONS, default = 'MAX') # max pooling is default?

    # job status
    QUEUED = 'Q'
    INPROGRESS = 'P'
    COMPLETED = 'C'
    JOB_STATUS_OPTIONS = (
        (QUEUED, "Queued"),
        (INPROGRESS, "In Progress"),
        (COMPLETED, "Completed")
    )
    job_status = models.CharField(max_length = 1, choices = JOB_STATUS_OPTIONS, default = QUEUED)

    # job times
    job_added = models.DateTimeField(default = datetime.now)
    job_start = models.DateTimeField(blank = True, null = True)
    job_completed = models.DateTimeField(blank = True, null = True)

    # currently returning to the job list page
    def get_absolute_url(self):
        return reverse('deepstyle:index', kwargs = None)

    # string repr. of the class
    def __str__(self):
        return self.job_name

    # define functions for differnet job status checks
    def is_queued(self):
        return self.job_status in (self.QUEUED)
    def is_inProgress(self):
        return self.job_status in (self.INPROGRESS)
    def is_completed(self):
        return self.job_status in (self.COMPLETED)
