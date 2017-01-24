from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from models import Course
from django.core.paginator import EmptyPage, InvalidPage
from digg_paginator import DiggPaginator as Paginator
import operator
import json

#index
def indexView(request):
    query = ''
    if 'query' in request.GET:
        query = request.GET['query']
    if not query or query=='':
        courses = Course.objects.all()
    else:
        qset = reduce(operator.__and__, [Q(course_name__icontains = query)])
        #| Q(descriptions__icontains = query) | \Q(provider__provider_name__icontains = query) | Q(school__school_name__icontains = query)])
        courses = Course.objects.filter(qset).distinct()
    provider = request.GET.get('provider')
    filterCourse(courses, provider)
    paginator = Paginator(courses, 7)
    page = request.GET.get('page')
    if (page==None):
        page = 1
    courses = getPaginatedCourses(page, paginator)
    return render(request, 'MOOCsite/index_extends.html', context={'courses': courses, 'page':page, 'queries': query})


def getPaginatedCourses(page, paginator):
    try:
        courses = paginator.page(page)
    except TypeError:
        # If page is not an integer, deliver first page.
        courses = None
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        courses = paginator.page(paginator.num_pages)
    return courses

def filterCourse(courses, provider):
    """
        if provider:
            qset = reduce(operator.__and__, [Q(provider__provider_name__icontains=provider)])
            courses = Course.objects.filter(qset).distinct()
    """
    if provider:
        qset = reduce(operator.__and__,[Q(provider__provider_name__icontains = provider)])
        courses = Course.objects.filter(qset).distinct()

def ajaxSearch2(request):
    query = request.GET['term']
    qset = reduce(operator.__and__, [Q(course_name__icontains = query)])
    #| Q(descriptions__icontains = query) | \Q(provider__provider_name__icontains = query) | Q(school__school_name__icontains = query)])
    courses = Course.objects.filter(qset).distinct()[:5]
    result = []
    for course in courses:
        course_json={}
        course_json['label'] = course.course_name
        course_json['value'] = course.course_name
        result.append(course_json)
    data = json.dumps(result)
    return HttpResponse(data,'application/json')


if __name__ == "__main__":
    print Course.object.all()
