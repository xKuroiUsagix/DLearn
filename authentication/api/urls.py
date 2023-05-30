from django.urls import path

from .views import ReceiveAuthToken, TestView


app_name = 'auth'

urlpatterns = [
    path('token/', ReceiveAuthToken.as_view(), name='token'),
    path('test/', TestView.as_view(), name='test'),
]
