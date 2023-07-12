from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify

class Post(models.Model):
    class TYPE(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        AUDIO = "AUDIO", "Audio"
        
    user = models.ForeignKey("Users.User", verbose_name=_("User"), on_delete=models.PROTECT)
    content = models.CharField(_("Content"), max_length=280)
    parent = models.ForeignKey('self', verbose_name=_("Replied to"), related_name="post_parent", on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(
        _("Slug"), default="", blank=False, null=False)
    media = models.FileField(_("Media"), upload_to='post/media/',
                             max_length=None, blank=True, null=True)
    media_type = models.CharField(
        _("Media type"), max_length=20, choices=TYPE.choices, null=True, blank=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from content, truncate to 50 characters
            self.slug = slugify(self.content)[:50]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")