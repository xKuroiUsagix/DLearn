from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView
)


app_name = 'task'
urlpatterns = [
    path('<int:course_id>/create-task/', login_required(TaskCreateView.as_view()), name='create'),
    path('<int:course_id>/task/<int:task_id>/', login_required(TaskDetailView.as_view()), name='detail'),
    path('<int:course_id>/task/<int:task_id>/delete/', login_required(TaskDeleteView.as_view()), name='delete')
]
