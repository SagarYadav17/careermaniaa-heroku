from rest_framework import serializers

from mania.models import *
from merchant_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_staff', 'is_merchant', 'is_verified', 'is_student']

class CoachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coaching
        fields = ('__all__')



class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('__all__')


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('__all__')
