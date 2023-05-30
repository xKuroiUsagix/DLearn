from authentication.models import CustomUser
from rest_framework.authtoken.models import Token


class TokensCreator:
    def run(self):
        for user in CustomUser.objects.all():
            Token.objects.get_or_create(user=user)
