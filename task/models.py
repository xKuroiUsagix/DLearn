import os
import uuid

from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dlearn.settings import MEDIA_ROOT
from course.models import Course
from authentication.models import CustomUser


def user_directory_path(instance, filename):
    return MEDIA_ROOT / f'users/user_{instance.user.id}/task_{instance.task.id}/{uuid.uuid1()}/{filename}'

def owner_directory_path(instance, filename):
    return MEDIA_ROOT / f'owners/owner_{instance.owner.id}/task_{instance.task.id}/{uuid.uuid1()}/{filename}'


class Task(models.Model):
    
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name=_('Course'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    do_up_to = models.DateTimeField(null=True, blank=True, verbose_name=_('Do Up To'))
    has_quiz = models.BooleanField(default=False, verbose_name=_('Has Quiz'))


class OwnerTaskFile(models.Model):
    
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE)
    task = models.ForeignKey(Task, on_delete=CASCADE)
    media = models.FileField(upload_to=owner_directory_path, null=True, blank=True, verbose_name=_('Media'), max_length=256)
    
    def __str__(self):
        return os.path.basename(self.media.name)

class UserTaskFile(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    task = models.ForeignKey(Task, on_delete=CASCADE)
    media = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name=_('Media'))


class UserTask(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('User'))
    task = models.ForeignKey(Task, on_delete=CASCADE, verbose_name=_('Task'))
    mark = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Mark'))
    done_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Done At'))
