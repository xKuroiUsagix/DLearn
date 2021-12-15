from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.utils.translation import gettext_lazy as _

from course.models import Course
from authentication.models import CustomUser


class Task(models.Model):
    
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name=_('Course'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    mark = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Mark'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    do_up_to = models.DateTimeField(null=True, blank=True, verbose_name=_('Do Up To'))


class OwnerTaskFile(models.Model):
    
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE)
    task = models.ForeignKey(Task, on_delete=CASCADE)
    media = models.FileField(upload_to='media', null=True, blank=True, verbose_name=_('Media'))


class UserTaskFile(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    task = models.ForeignKey(Task, on_delete=CASCADE)
    media = models.FileField(upload_to='media', null=True, blank=True, verbose_name=_('Media'))
