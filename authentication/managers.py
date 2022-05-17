from typing import ValuesView
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


from .errors import ErrorMessages


class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValuesView(ErrorMessages.EMAIL_NOT_GIVEN_ERROR)
        
        email = self.normalize_email(email)
        if extra_fields.get('confirm_password') is not None:
            extra_fields.pop('confirm_password')
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)
        
        if extra_fields.get('role') != 1:
            raise ValueError(ErrorMessages.SUPERUSER_ROLE_ERROR)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ErrorMessages.SUPERUSER_IS_SUPERUSER_ERROR)
        return self.create_user(email, password, **extra_fields)
