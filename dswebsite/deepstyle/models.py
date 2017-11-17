from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

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

    # input_image = models.ForeignKey(Image, blank = False, null = "False", related_name='+')
    # style_image = models.ForeignKey(Image, blank = False, null = "False",  related_name='+')

    input_image = models.ImageField(blank = False, null = True, max_length=500, verbose_name= ('Input Image (Uplaoding large images may take a while.)'))
    style_image = models.ImageField(blank = False, null = True, max_length=500, verbose_name = ('Style Image (Uploading large images may take a while.)'))
    output_image = models.CharField(max_length = 500, blank = True, null = True)

    # parameters for running a job
    # TOFIX: add more restricted limit to each param?
    output_width = models.PositiveSmallIntegerField(
        default = 600,
        verbose_name= ('Output Width [100 - 1000] (Higher width will output higher resolution image, however, at higher processing time)'),
        validators=[MaxValueValidator(1000, message="Value too high"), MinValueValidator(100, message="Value too low")],
        )
    iterations = models.PositiveIntegerField(
        default = 1000,
        verbose_name= ('Iterations [500 - 3000] (Higher iterations might output better results, however, at higher processing time)'),
        validators=[MaxValueValidator(3000, message="Value too high"), MinValueValidator(500, message="Value too low")],
        )
    content_weight = models.FloatField(
        default = 5e0,
        verbose_name= ('Content Weight [Any value relative to style weight]')
        )
    content_weight_blend = models.FloatField(
        default = 1,
        verbose_name= ('Content Weight Blend [0.0 - 1.0]'),
        validators=[MaxValueValidator(1.0, message="Value too high"), MinValueValidator(0.0, message="Value too low")],
        )
    style_weight = models.FloatField(default = 5e2, verbose_name= ('Style Weight [Any value relative to content weight]'))
    style_blend_weights = models.FloatField(
        default = 1,
        verbose_name= ('Style Blend Weights [0.0 - 1.0]'),
        validators=[MaxValueValidator(1.0, message="Value too high"), MinValueValidator(0.0, message="Value too low")],
    )
    style_scale = models.FloatField(default = 1.0, verbose_name= ('Style Scale [~0.5 - ~2.0]'))
    learning_rate = models.FloatField(default = 1e1, verbose_name= ('Learning Rate [~10] (Best kept at default)'))
    style_layer_weight_exp = models.FloatField(default = 1, verbose_name= ('Style Layer Weight Exp [Any value] (Lower value results in more detailed output)'))
    preserve_color = models.BooleanField(default = False)

    # pooling
    POOLING_OPTIONS = (
        ('MAX', "max"),
        ('AVG', "avg")
    )
    pooling = models.CharField(max_length = 3, choices = POOLING_OPTIONS, default = 'MAX')

    # job status
    QUEUED = 'Q'
    INPROGRESS = 'P'
    COMPLETED = 'C'
    FAIL = 'F'
    PROGRESS_FAIL = 'PF'
    JOB_STATUS_OPTIONS = (
        (QUEUED, "Queued"),
        (INPROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (FAIL, "Failed"),
        (PROGRESS_FAIL, "Progress Failed"),
    )
    job_status = models.CharField(max_length = 2, choices = JOB_STATUS_OPTIONS, default = QUEUED)

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
