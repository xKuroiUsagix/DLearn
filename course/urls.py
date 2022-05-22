from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    CourseCreateView,
    CourseJoinView,
    CourseDetailView,
    CourseUpdateView,
    UserCourseView,
    LeaveCourseView,
    KickUserView,
    CourseListView
)


app_name = 'course'
urlpatterns = [
    path('create/', login_required(CourseCreateView.as_view()), name='create'),
    path('join/', login_required(CourseJoinView.as_view()), name='join'),
    path('<int:pk>/', login_required(CourseDetailView.as_view()), name='detail'),
    path('my-courses/', login_required(CourseListView.as_view()), name='list'),
    path('<int:pk>/settings/', login_required(CourseUpdateView.as_view()), name='settings'),
    path('<int:course_id>/users/', login_required(UserCourseView.as_view()), name='users'),
    path('<int:course_id>/kick_user/<int:user_id>/', login_required(KickUserView.as_view()), name='kick_user'),
    path('<int:course_id>/leave/', login_required(LeaveCourseView.as_view()), name='leave'),
]
