from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .constants import ROLE_CHOICES


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        This class represents a basic user.\n
        Attributes:
        ----------
        param email: Describes the email of the user
        type email: str, unique, max_length=40
        param password: Describes the password of the user
        type password: str, max_length=255
        param first_name: Describes the first name of the user
        type first_name: str, max_length=30, null=True
        param last_name: Describes the last name of the user
        type last_name: str, max_length=30, null=True
        param created_at: Describes the date when the user was created. Can't be changed
        type created_at: int (timestamp)
        param role: Describes the role of the user
        type role: int, default=0
    """
    email = models.EmailField(verbose_name=_('Email'), max_length=40, unique=True, validators=[validate_email])
    password = models.CharField(verbose_name=_('Password'), max_length=255)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=30, null=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=30, null=True)
    created_at = models.DateField(verbose_name=_('CreatedAt'), auto_now_add=True)
    role = models.IntegerField(default=0, choices=ROLE_CHOICES)
    
    USERNAME_FIELD = 'email'
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
