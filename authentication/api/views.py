from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import AuthTokenSerializer


class ReceiveAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
