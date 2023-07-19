import re
from django.db import models
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField
from django.contrib.contenttypes.fields import GenericRelation
from HashTags.models import HashTag


class Post(models.Model):
    class TYPE(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        AUDIO = "AUDIO", "Audio"

    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.PROTECT, blank=True, null=True)
    content = models.TextField(_("Content"), blank=True, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_(
        "Replied to"), related_name="post_parent", on_delete=models.CASCADE, null=True, blank=True)
    slug = AutoSlugField(_("Slug"), populate_from=['title'])
    media = models.FileField(_("Media"), upload_to='post/media/',
                             max_length=None, blank=True, null=True)
    hashtags = models.ManyToManyField(
        "HashTags.HashTag", blank=True, db_index=True)
    reactions = GenericRelation("Reactions.Reaction")
    media_type = models.CharField(
        _("Media type"), max_length=20, choices=TYPE.choices, null=True, blank=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(
        _("Edited date"), blank=True, null=True, auto_now=True)

    def __str__(self):
        return f"{self.user.user_name}: {self.content}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.process_hashtags()

    def process_hashtags(self):
        existing_hashtags = self.hashtags.all()

        # Extract hashtags from content
        hashtags = re.findall(r'#\w+', self.content)

        # Remove the '#' symbol from the tag
        for tag_text in hashtags:
            tag_name = tag_text[1:]

            # Check if the tag already exists
            existing_tag = existing_hashtags.filter(tag=tag_name).first()

            if not existing_tag:
                # Get or create the hashtag
                hashtag, _ = HashTag.objects.get_or_create(tag=tag_name)

                # Associate the hashtag with the post
                self.hashtags.add(hashtag)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")