from django.db import models
from django.utils.translation import gettext as _


class HashTag(models.Model):
    '''
    HashTag model to be used in posts and articles
    '''
    tag = models.CharField(_("tag"), max_length=255, blank=False, null=True)
    created_date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("HashTag")
        verbose_name_plural = _("HashTags")


class Engagement(models.Model):
    '''
    Simple model to save the analyzed data about hashtag performance
    '''
    tag = models.ForeignKey("HashTag", verbose_name=_(
        "Hashtag"), on_delete=models.PROTECT, blank=False, null=True)
    date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)
    duration = models.DurationField(_("Duration"), blank=True, null=True)
    int_amount = models.PositiveIntegerField(
        _("Interaction amount"), default=0, blank=False, null=True)

    class Meta:
        verbose_name = _("Engagement statistic")
        verbose_name_plural = _("Engagement statistics")
