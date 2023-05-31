from django.urls import path

from .views import ReceiveAuthToken


app_name = 'auth_api'

urlpatterns = [
    path('token/', ReceiveAuthToken.as_view(), name='token'),
]
