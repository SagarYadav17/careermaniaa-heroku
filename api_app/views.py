from rest_framework import viewsets

from mania.models import *
from merchant_app.models import *
from api_app.serializer import *

# Create your views here.


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserAPI


class MerchantDetailSAPIView(viewsets.ModelViewSet):
    queryset = Merchant_Details.objects.all().order_by('-id')
    serializer_class = MerchantDetailsAPI


class CoachingAPIView(viewsets.ModelViewSet):
    queryset = Coaching.objects.all().order_by('-id')
    serializer_class = CoachingAPI


class BranchAPIView(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('-id')
    serializer_class = BranchAPI


class CourseAPIView(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseAPI


class CollegeAPIView(viewsets.ModelViewSet):
    queryset = College.objects.all().order_by('-id')
    serializer_class = CollegeAPI

class JobAPIView(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-id')
    serializer_class = JobAPI
