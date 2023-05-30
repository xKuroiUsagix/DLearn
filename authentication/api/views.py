from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AuthTokenSerializer


class ReceiveAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class TestView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        return Response(['works', request.user.email, request.user.password])
