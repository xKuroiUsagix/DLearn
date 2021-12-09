from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomUser


class Course(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=128)
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('Owner'))
    group_name = models.CharField(max_length=60, null=True, blank=True, verbose_name=_('GroupName'))
    join_code = models.CharField(max_length=20, unique=True, verbose_name=_('JoinCode'))
    password = models.CharField(max_length=128,  verbose_name=_('Password'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_('CreatedAt'))


class UserCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('User'))
    course = models.ForeignKey(Course, on_delete=DO_NOTHING, verbose_name=_('Course'))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_('JoinedAt'))
