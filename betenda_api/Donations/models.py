from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class Campaign(models.Model):
    reason = models.CharField(_("Reason for donation"), max_length=255)
    amount_needed = models.PositiveIntegerField(_("Amount needed"))
    amount_donated = models.PositiveIntegerField(_("Amount donated(achieved)"))
    campaign_start = models.DateTimeField(
        _("Campaign set on"), auto_now=False, auto_now_add=True)
    campaign_end = models.DateTimeField(
        _("Ideal achievement date"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.reason}[:15].., {self.amount_needed}/{self.amount_donated}"

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
