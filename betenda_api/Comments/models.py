from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(
        "Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    comment = models.TextField(_("Comment"), blank=False)
    parent = models.ForeignKey("Comment", verbose_name=_("Replied to"), related_name="comment_parent", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated date"), auto_now=True)
    
    reactions = GenericRelation("Reactions.Reaction")

    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Content type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("Object id"))
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.comment[:15]}.. by @{self.user.user_name}'

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")