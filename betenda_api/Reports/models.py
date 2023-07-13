from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _


# Create your models here.
class Report(models.Model):
    TYPE = (
        ('TYPE1', 'Type 1'),
        ('TYPE2', 'Type 2'),
        ('TYPE3', 'Type 3'),
        ('TYPE4', 'Type 4'),
        ('TYPE5', 'Type 5'),
        ('TYPE6', 'Type 6'),
    )
    # user foreignkey optional
    user = models.ForeignKey(
        "Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    report = models.TextField(_("Comment"), blank=False, null=True)
    report_type = models.CharField(_("Report type"), max_length=255, choices=TYPE)
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
