from django.urls import path, include
from api_app import views

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/', views.apiOverview, name='api'),
    path('users/', views.userList, name='user-list'),
    path('coachings/', views.coachingList, name='coaching-list'),
    path('colleges/', views.collegeList, name='college-list'),
    path('jobs/', views.jobList, name='job-list'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
