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


class Donation(models.Model):
    user = models.ForeignKey(
        "Users.User", verbose_name=_("Donator"), on_delete=models.CASCADE)
    donation_amount = models.PositiveIntegerField(_("Donation amount"))
    donation_for = models.ForeignKey("Campaign", verbose_name=_(
        "Donation cause"), blank=True, null=True, on_delete=models.CASCADE)
    remark = models.CharField(_("Remark"), max_length=255)
    donation_date = models.DateTimeField(
        _("Donation date"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.donation_amount} for {self.donation_for} on {self.donation_date}"

    class Meta:
        verbose_name = _("Donation")
        verbose_name_plural = _("Donations")
