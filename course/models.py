from email.policy import default
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

from dlearn.settings import MEDIA_ROOT
from authentication.models import CustomUser

import uuid


DEFAULT_IMAGE_PATH = MEDIA_ROOT / f'default/default_image.png'


def course_directory_path(instance, filename):
    return MEDIA_ROOT / f'courses/course_{instance.id}/{uuid.uuid1()}/{filename}'


class Course(models.Model):
    """
        This class represents a course owned by some user.\n
        Attributes:
        ----------
        param name: Describes the name of the course
        type email: str, max_length=128
        param owner: Describes the owner of the course
        type owner: int, CustomUser, on_delete=CASCADE
        param group_name: Describes the group name of the course
        type group_name: str, max_length=60, null=True, blank=True
        param join_code: Describes the code for joining the course (same as login for user account)
        type join_code: str, max_length=20, unique=True
        param password: Describes the password for the course to join
        type password: str, max_length=128
        param created_at: Describes the date when the course was created
        type created_at: timestamp, auto_now_add=True
    """
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    owner = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('Owner'))
    group_name = models.CharField(max_length=60, null=True, blank=True, verbose_name=_('GroupName'))
    join_code = models.CharField(max_length=20, unique=True, verbose_name=_('JoinCode'))
    image = models.ImageField(upload_to=course_directory_path, null=False, blank=False, max_length=256, default=DEFAULT_IMAGE_PATH)
    password = models.CharField(max_length=128,  verbose_name=_('Password'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_('CreatedAt'))
    
    _password = None
    
    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        """Sets the course password

        Args:
            raw_password (str): raw password of the course
        """
        self.password = make_password(raw_password)
        self._password = raw_password
        
    def check_password(self, raw_password):
        """Cheks the raw_password with course password

        Args:
            raw_password (str): potential password of the course
            
        Return:
            bool: True if password and raw_password same, else False
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=['password'])
        return check_password(raw_password, self.password, setter)


class UserCourse(models.Model):
    """
        This class represents an information about users and courses to which they belong to.\n
        Attributes:
        ----------
        param user: Describes the user that belongs to the course
        type user: int, CustomUser, on_delete=CASCADE
        param course: Describes the course to which the user belongs to
        type course: int, Course, on_delete=CASCADE
        param joined_at: Describes the date and time when the user joined to the course
        type joined_at: timestamp, auto_now_add=True
    """
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, verbose_name=_('User'))
    course = models.ForeignKey(Course, on_delete=CASCADE, verbose_name=_('Course'))
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name=_('JoinedAt'))
