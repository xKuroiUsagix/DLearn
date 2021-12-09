from django.urls import path

from .views import CreateCourseView

app_name = 'course'
urlpatterns = [
    path('create/', CreateCourseView.as_view(), name='create')
]
