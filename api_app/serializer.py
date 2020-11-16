from rest_framework import serializers

from mania.models import *
from merchant_app.models import *


class UserAPI(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'name']


class MerchantDetailsAPI(serializers.ModelSerializer):
    class Meta:
        model = Merchant_Details
        fields = ('__all__')


class CoachingAPI(serializers.ModelSerializer):
    class Meta:
        model = Coaching
        fields = ('__all__')


class BranchAPI(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')


class CourseAPI(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('__all__')



class CollegeAPI(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('__all__')

class JobAPI(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('__all__')
