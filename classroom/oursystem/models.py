from django.db import models

# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify
import os
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subject_id)
        super().save(*args, **kwargs)


def save_course_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.course_id:
        filename = 'course_files/{}/{}.{}'.format(instance.course_id,instance.course_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.course_id) + str('1')
            filename =  'course_images/{}/{}.{}'.format(instance.course_id,new_name, ext)
    return os.path.join(upload_to, filename)


class Course(models.Model):
    course_id = models.CharField(max_length=100,)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=7, auto_created=True, unique=True)
    section = models.PositiveSmallIntegerField(verbose_name="Section no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_course_files,verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to=save_course_files,verbose_name="Presentations", blank=True)
    pdf = models.FileField(upload_to=save_course_files,verbose_name="pdf", blank=True)

    class Meta:
        ordering = ['section']
        ordering=['code']
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('oursystem:course_list', kwargs={'slug':self.subject.slug })
        

    

class Comment(models.Model):
    course_name = models.ForeignKey(Course, null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)


