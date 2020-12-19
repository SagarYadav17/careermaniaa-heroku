from django.urls import path, include
from api_app import views

urlpatterns = [
    path('api/', views.apiOverview, name='api'),
    path('api/users/', views.userList, name='user-list'),
    path('api/coachings/', views.coachingList, name='coaching-list'),
    path('api/colleges/', views.collegeList, name='college-list'),
    path('api/jobs/', views.jobList, name='job-list'),
]
