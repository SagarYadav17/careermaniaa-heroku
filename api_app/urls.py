from django.urls import path, include
from api_app import views

urlpatterns = [
    path('api/', views.apiOverview, name='api'),
    path('users/', views.userList, name='user-list'),
    path('coachings/', views.coachingList, name='coaching-list'),
    path('colleges/', views.collegeList, name='college-list'),
    path('jobs/', views.jobList, name='job-list'),
]
        