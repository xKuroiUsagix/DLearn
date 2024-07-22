from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Course


@receiver(post_delete, sender=Course)
def remove_course_image_from_s3(sender, instance, *args, **kwargs):
    instance.image.delete(save=False)
