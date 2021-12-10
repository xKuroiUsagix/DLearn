from django.contrib.auth.hashers import check_password, make_password
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
    
    _password = None
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password
        
    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=['password'])
        return check_password(raw_password, self.password, setter)


class UserCourse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('User'))
    course = models.ForeignKey(Course, on_delete=DO_NOTHING, verbose_name=_('Course'))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_('JoinedAt'))
