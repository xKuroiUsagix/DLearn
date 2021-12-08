from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.utils import DataError
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


ROLE_CHOICES = (
    (0, 'common_user'),
    (1, 'admin')
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(verbose_name=_('Email'), max_length=40, unique=True, validators=[validate_email])
    password = models.CharField(verbose_name=_('Password'), max_length=255)
    first_name = models.CharField(verbose_name=_('FirstName'), max_length=30, null=True)
    last_name = models.CharField(verbose_name=_('LastName'), max_length=30, null=True)
    patronymic = models.CharField(verbose_name=_('Patronymic'), max_length=30, null=True)
    created_at = models.DateField(verbose_name=_('CreatedAt'), auto_now_add=True)
    role = models.IntegerField(default=0, choices=ROLE_CHOICES)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    objects = UserManager()
