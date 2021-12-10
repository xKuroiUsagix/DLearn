from django.urls import path

from .views import CourseCreateView, CourseJoinView

app_name = 'course'
urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='create'),
    path('join/', CourseJoinView.as_view(), name='join'),
]
