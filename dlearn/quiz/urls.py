from django.urls import path

from .views import QuizCreateView, QuizDetailView, UserDetailView


app_name = 'quiz'
urlpatterns = [
    path('<int:course_id>/task/<int:task_id>/create-quiz/', view=QuizCreateView.as_view(), name='create'),
    path('<int:course_id>/task/<int:task_id>/quiz/', view=QuizDetailView.as_view(), name='detail'),
    path('<int:course_id>/task/<int:task_id>/quiz/user-detail/<int:user_id>/', view=UserDetailView.as_view(), name='user_detail')
]

