from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    CourseCreateView,
    CourseJoinView,
    CourseDetailView,
    CourseUpdateView,
    OwnedCoursesView,
    KickUserView,
    JoinedCoursesView,
    LeaveCourseView,
)


app_name = 'course'
urlpatterns = [
    path('create/', login_required(CourseCreateView.as_view()), name='create'),
    path('join/', login_required(CourseJoinView.as_view()), name='join'),
    path('owned-courses/', login_required(OwnedCoursesView.as_view()), name='owned_courses'),
    path('joined-courses/', login_required(JoinedCoursesView.as_view()), name='joined_courses'),
    path('<int:pk>/', login_required(CourseDetailView.as_view()), name='detail'),
    path('<int:pk>/settings/', login_required(CourseUpdateView.as_view()), name='settings'),
    path('<int:course_id>/delete-user/<int:user_id>', login_required(KickUserView.as_view()), name='kick_user'),
    path('<int:course_id>/leave/', login_required(LeaveCourseView.as_view()), name='leave'),
]
