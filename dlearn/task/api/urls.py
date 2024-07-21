from django.urls import path

from .views import TaskAPIView, UserFilesAPIView, OwnerFilesAPIView, TaskListAPIView


app_name='task_api'

urlpatterns = [
    path('', TaskAPIView.as_view(), name='detail'),
    path('list/', TaskListAPIView.as_view(), name='list'),
    path('user-files/', UserFilesAPIView.as_view(), name='user_files'),
    path('owner-files/', OwnerFilesAPIView.as_view(), name='owner_files')
]
