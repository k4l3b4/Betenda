from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

# Create your models here.
class BookMark(models.Model):
    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.CASCADE, blank=False, db_index=True)
    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Content type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("Object id"))
    content_object = GenericForeignKey('content_type', 'object_id')
    added_date = models.DateTimeField(_("Added date"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name=_("BookMark")
        verbose_name_plural=_("BookMark")

    def __str__(self):
        return f"{self.content_type}:{self.object_id}"