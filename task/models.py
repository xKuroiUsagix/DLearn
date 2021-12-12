from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from course.models import Course


class Task(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name=_('Course'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    mark = models.IntegerField(null=True, blank=True, verbose_name=_('Mark'))
    files = models.FileField(null=True, blank=True, verbose_name=_('Files'))
