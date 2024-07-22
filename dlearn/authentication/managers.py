from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from .errors import ErrorMessages


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError(ErrorMessages.EMAIL_NOT_GIVEN_ERROR)
        
        email = self.normalize_email(email)
        extra_fields.pop('confirm_password', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
