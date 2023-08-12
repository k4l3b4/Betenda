import re
from django.db import models
from django.utils.translation import gettext as _
from filemime import filemime
from django_extensions.db.fields import RandomCharField
from django.contrib.contenttypes.fields import GenericRelation
from HashTags.models import HashTag
from django.dispatch import receiver

class Post(models.Model):
    allowed_image_types = ['image/jpg', 'image/jpeg', 'image/png', 'image/webp', 'image/gif']
    allowed_video_types = ['video/mp4', 'video/mkv']

    class TYPE(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        AUDIO = "AUDIO", "Audio"

    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.PROTECT, blank=True, null=True, db_index=True)
    content = models.TextField(_("Content"), blank=True, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_(
        "Replied to"), related_name="post_parent", on_delete=models.CASCADE, null=True, blank=True)
    slug = RandomCharField(
        _("Slug"), length=20, unique=True, include_alpha=False)
    media = models.FileField(_("Media"), upload_to='post/media/',
                             max_length=None, blank=True, null=True)
    hashtags = models.ManyToManyField(
        "HashTags.HashTag", blank=True, db_index=True)
    reactions = GenericRelation("Reactions.Reaction")
    report = GenericRelation("Reports.Report")
    media_type = models.CharField(
        _("Media type"), max_length=20, choices=TYPE.choices, null=True, blank=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(
        _("Edited date"), blank=True, null=True, auto_now=True)

    def __str__(self):
        return f"{self.user.user_name}: {self.content}"

    def save(self, *args, **kwargs):
        self.process_media_type()
        super().save(*args, **kwargs)
        self.process_hashtags()

    def process_hashtags(self):
        existing_hashtags = self.hashtags.all()
        # Extract hashtags from content
        hashtags = re.findall(r'#\w+', self.content)
        # Remove the '#' symbol from the tag
        for tag_text in hashtags:
            tag_name = tag_text[1:]
            existing_tag = existing_hashtags.filter(tag=tag_name).first()
            if not existing_tag:
                hashtag, _ = HashTag.objects.get_or_create(tag=tag_name)
                self.hashtags.add(hashtag)

    def process_media_type(self):
        if self.media:
            read_size = 5 * (1024 * 1024)

            from magic import from_buffer

            mime = from_buffer(self.media.read(read_size), mime=True)
            print("mime:", mime)

            if mime in self.allowed_image_types:
                self.media_type = self.TYPE.IMAGE
            elif mime in self.allowed_video_types:
                self.media_type = self.TYPE.VIDEO
        
    @receiver(models.signals.pre_save, sender="Posts.Post")
    def server_delete_files(sender, instance, **kwargs):
        if instance.id is not None:
            for field in instance._meta.fields:
                if field.name == "media":
                    file = getattr(instance, field.name)
                    if file:
                        file.delete(save=False)


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
