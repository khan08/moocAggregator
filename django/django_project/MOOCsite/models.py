from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Provider(models.Model):
    provider_name = models.CharField(max_length=200, unique=True)


class School(models.Model):
    # crs_Pid = models.CharField(max_length=200,unique=True)
    school_name = models.CharField(max_length=200, unique=True)


class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)


class Course(models.Model):
    # foreign keys
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    # course details
    photo_url = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    descriptions = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.course_name


class Time(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    isSelf = models.NullBooleanField(null=True)
    duration = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = ('course', 'startDate')


'''
class Instructors(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    bio = models.CharField(max_length=200,null='')
    name = models.CharField(max_length=200)
    '''
