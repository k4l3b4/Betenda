from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericRelation


class HashTag(models.Model):
    '''
    HashTag model to be used in posts and articles
    '''
    tag = models.CharField(_("tag"), max_length=255, blank=False, null=True)
    created_date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)
    report = GenericRelation("Reports.Report")

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
    hashtag = models.ForeignKey('HashTag', related_name="user_tag", on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    subscribed_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.user.user_name}: {self.hashtag} {self.score}"
    
    class Meta:
        verbose_name = _("User hashtag")
        verbose_name_plural = _("User hashtags")

class Engagement(models.Model):
    '''
    Simple model to save the analyzed data about hashtag performance
    '''
    tag = models.ForeignKey("HashTag", verbose_name=_(
        "Hashtag"), on_delete=models.PROTECT, blank=False, null=True)
    date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)
    frequency = models.DecimalField(
        _("Interaction amount"), default=0.01, decimal_places=2, max_digits=3, blank=False, null=True)
    int_amount = models.PositiveIntegerField(
        _("Interaction amount"), default=0, blank=False, null=True)
    
    def __str__(self):
        return f"{self.tag}: {self.int_amount} {self.date}"

    class Meta:
        verbose_name = _("Engagement statistic")
        verbose_name_plural = _("Engagement statistics")