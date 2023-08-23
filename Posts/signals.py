import os
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from betenda_api.methods import generate_thumbnail
from .models import Post


@receiver(pre_save, sender=Post)
def generate_thumbnail_on_save(sender, instance, **kwargs):
    if instance.media:
        try:
            thumbnail_name = os.path.splitext(os.path.basename(instance.media.name))[0] + '_thumbnail.jpg'
            thumbnail_path = os.path.join('thumbnails', thumbnail_name)
            thumbnail_full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
            
            if generate_thumbnail(instance.media.path, thumbnail_full_path):
                instance.thumbnail = thumbnail_path
        except Exception as e:
            print("Error generating thumbnail on save:", str(e))