from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _


# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(
        "Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    report = models.TextField(_("Comment"), blank=True, null=True)
    # not a list of predefined choices to make it flexible, optional choices will be coded in the frontend
    report_type = models.CharField(_("Report type"), max_length=255)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Content type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("Object id"))
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"@{self.user.user_name}'s report on {self.content_object}"

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")