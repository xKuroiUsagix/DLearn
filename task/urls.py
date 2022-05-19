from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    DeleteOwnerFileView,
    DeleteUserFileView,
    AddUserFilesView,
    UserFilesListView,
    UserRatingView
)


app_name = 'task'
urlpatterns = [
    path('<int:course_id>/create-task/', login_required(TaskCreateView.as_view()), name='create'),
    path('<int:course_id>/task/<int:task_id>/', login_required(TaskDetailView.as_view()), name='detail'),
    path('<int:course_id>/task/<int:task_id>/delete/', login_required(TaskDeleteView.as_view()), name='delete'),
    path('<int:course_id>/task/<int:task_id>/edit/', login_required(TaskUpdateView.as_view()), name='edit'),
    path('<int:course_id>/task/<int:task_id>/delete-owner-file/<int:file_id>/', 
         login_required(DeleteOwnerFileView.as_view()),
         name='delete_owner_file'
    ),
    path('<int:course_id>/task/<int:task_id>/delete-user-file/<int:file_id>/',
         login_required(DeleteUserFileView.as_view()),
         name='delete_user_file'
    ),
    path('<int:course_id>/task/<int:task_id>/add-files/', login_required(AddUserFilesView.as_view()), name='add_files'),
    path('<int:course_id>/task/<int:task_id>/user-files/', login_required(UserFilesListView.as_view()), name='user_files'),
    path('<int:course_id>/task/<int:task_id>/user-rating/', login_required(UserRatingView.as_view()), name='user_rating')
]
