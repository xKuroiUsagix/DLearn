from django.urls import path

from .views import QuizCreateView, QuizDetailView


app_name = 'quiz'
urlpatterns = [
    path('<int:course_id>/task/<int:task_id>/create-quiz/', view=QuizCreateView.as_view(), name='create'),
    path('<int:course_id>/task/<int:task_id>/quiz/', view=QuizDetailView.as_view(), name='detail')
]

