from mania.models import *
from merchant_app.models import *
from api_app.serializer import *

from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Users': '/users/',
        'Coachings': '/coachings/',
        'Colleges': '/colleges/',
        'Jobs': '/jobs/',
    }

    return Response(api_urls)


@api_view(['GET'])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def coachingList(request):
    coaching = Coaching.objects.all()
    serializer = CoachingSerializer(coaching, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def collegeList(request):
    college = College.objects.all()
    serializer = CollegeSerializer(college, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def jobList(request):
    job = Job.objects.all()
    serializer = JobSerializer(job, many=True)
    return Response(serializer.data)
