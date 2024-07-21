from django.urls import path

from .views import (
    CourseAPIView, 
    CourseListAPIView, 
    CourseUpdateAPIView,
    JoinCourseAPIVIew,
    LeaveCourseAPIView
)


app_name = 'course_api'

urlpatterns = [
    path('', CourseAPIView.as_view(), name='course'),
    path('update/', CourseUpdateAPIView.as_view(), name='update'),
    path('join/', JoinCourseAPIVIew.as_view(), name='join'),
    path('leave/', LeaveCourseAPIView.as_view(), name='leave'),
    path('list/', CourseListAPIView.as_view(), name='course_list'),
]
