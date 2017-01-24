from django.test import TestCase
from models import Course, School, Provider, Time
# Create your tests here.
regex = 'java'
    # regex = re.sub('\s+','|',text).strip()
    # regex = re.sub('\s+','|',text).strip()
courses = Course.objects.filter(course_name__iregex=regex).values_list('school_name')