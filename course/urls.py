from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    CourseCreateView,
    CourseJoinView,
    OwnedCoursesView,
    JoinedCoursesView,
    CourseDetailView,
    CourseUpdateView,
)


app_name = 'course'
urlpatterns = [
    path('create/', login_required(CourseCreateView.as_view()), name='create'),
    path('join/', login_required(CourseJoinView.as_view()), name='join'),
    path('owned-courses/', login_required(OwnedCoursesView.as_view()), name='owned_courses'),
    path('joined-courses/', login_required(JoinedCoursesView.as_view()), name='joined_courses'),
    path('<int:pk>/', login_required(CourseDetailView.as_view()), name='detail'),
    path('<int:pk>/settings/', login_required(CourseUpdateView.as_view()), name='settings'),
]
