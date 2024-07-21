from django.urls import path

from .views import (
    CourseCreateView,
    CourseJoinView,
    CourseDetailView,
    CourseDeleteView,
    CourseUpdateView,
    UserCourseView,
    LeaveCourseView,
    KickUserView
)


app_name = 'course'
urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='create'),
    path('join/', CourseJoinView.as_view(), name='join'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('<int:course_id>/delete/', CourseDeleteView.as_view(), name='delete'),
    path('<int:course_id>/settings/', CourseUpdateView.as_view(), name='settings'),
    path('<int:course_id>/users/', UserCourseView.as_view(), name='users'),
    path('<int:course_id>/kick_user/<int:user_id>/', KickUserView.as_view(), name='kick_user'),
    path('<int:course_id>/leave/', LeaveCourseView.as_view(), name='leave'),
]
