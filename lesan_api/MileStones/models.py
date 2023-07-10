from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class MileStoneType(models.Model):
    TYPE_CHOICES = (
        ('10_invites', 'Get to your invitation threshold'),
        ('100_words', 'Contribute 100 words'),
        ('1000_words', 'Contribute 1000 words'),
        ('5000_words', 'Contribute 5000 words'),
        ('10000_words', 'Contribute 10000 words'),
        ('15000_words', 'Contribute 15000 words'),
        ('20000_words', 'Contribute 20000 words'),
        ('25000_words', 'Contribute 25000 words'),
        ('30000_words', 'Contribute 30000 words'),
        ('write_a_poem', 'The poet'),
        ('write_5_poem', 'Descendant of Walt Whitman'),
        ('write_10_poem', 'Descendant of Walt Whitman'),
        ('write_15_poem', 'Descendant of Emily Dickson'),
        ('write_50_poem', 'Descendant of Emily Dickson'),
    )

    milestone_type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    milestone_desc = models.CharField(max_length=255, blank=False, null=True)
    milestone_pic = models.ImageField(
        _("Milestone picture"), upload_to='milestone/', max_length=None, blank=False, null=True)


class MileStone(models.Model):
    user = models.ForeignKey(
        "Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    milestone = models.ForeignKey(
        "MileStoneType", verbose_name=_(""), on_delete=models.CASCADE)
    achievement_date = models.DateTimeField(
        _("Achievement date"), auto_now=False, auto_now_add=True)
