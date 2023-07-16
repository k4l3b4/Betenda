from django.db import models
from django.utils.translation import gettext as _


class HashTag(models.Model):
    '''
    HashTag model to be used in posts and articles
    '''
    tag = models.CharField(_("tag"), max_length=255, blank=False, null=True)
    created_date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.tag}"
    
    class Meta:
        verbose_name = _("HashTag")
        verbose_name_plural = _("HashTags")


class UserHashtag(models.Model):
    '''
    Tags a user has subscribed to
    '''
    user = models.ForeignKey("Users.User", on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
    score = models.IntegerField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name}: {self.hashtag} {self.score}"

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
    
    def __str__(self):
        return f"{self.tag}: {self.int_amount} {self.date}"

    class Meta:
        verbose_name = _("Engagement statistic")
        verbose_name_plural = _("Engagement statistics")
