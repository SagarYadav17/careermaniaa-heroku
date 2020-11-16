from django.urls import path, include
from api_app import views

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=True)
router.register('users', views.UserAPIView)
router.register('merchant-detail', views.MerchantDetailSAPIView)
router.register('coaching', views.CoachingAPIView)
router.register('branch', views.BranchAPIView)
router.register('college', views.CollegeAPIView)
router.register('job', views.JobAPIView)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
        