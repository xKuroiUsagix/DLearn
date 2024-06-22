from django.urls import path

from .views import (
    QuizAPIView, 
    QuestionAPIVIew, 
    OptionAPiView, 
    StartQuizAPIView, 
    QuestionSelectOptionsAPIView,
    QuestionAddTextAnswer,
    QuestionSetMark,
    CountMarkForQuiz,
    UserResultAPIView,
    ResultDetailAPIView
)


app_name = 'quiz_api'

urlpatterns = [
    path('', QuizAPIView.as_view(), name='quiz'),
    path('user-result/', UserResultAPIView.as_view(), name='user_result'),
    path('start/', StartQuizAPIView.as_view(), name='start'),
    path('question/', QuestionAPIVIew.as_view(), name='question'),
    path('question/option/', OptionAPiView.as_view(), name='option'),
    path('question/select-options/', QuestionSelectOptionsAPIView.as_view(), name='select_options'),
    path('question/add-text-answer/', QuestionAddTextAnswer.as_view(), name='add_text_answer'),
    path('question/set-mark/', QuestionSetMark.as_view(), name='set_mark'),
    path('count-mark/', CountMarkForQuiz.as_view(), name='count_mark'),
    path('all-results/', ResultDetailAPIView.as_view(), name='result_detail')
]
