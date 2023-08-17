from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


TYPE_CHOICES = (
        ('10_invites', 'Get to your invitation limit'),
        
        ('10_words', 'Contribute 10 words'),
        ('20_words', 'Contribute 20 words'),
        ('50_words', 'Contribute 50 words'),
        ('100_words', 'Contribute 100 words'),
        ('1000_words', 'Contribute 1000 words'),
        ('5000_words', 'Contribute 5000 words'),
        ('10000_words', 'Contribute 10000 words'),
        ('15000_words', 'Contribute 15000 words'),
        ('20000_words', 'Contribute 20000 words'),
        ('25000_words', 'Contribute 25000 words'),
        ('30000_words', 'Contribute 30000 words'),

        ('write_a_poem', 'Write a poem'),
        ('write_5_poem', 'Write 5 poems'),
        ('write_15_poem', 'Write 15 poems'),
        ('write_50_poem', 'Write 50 poems'),

        ('write_10_sayings', 'Write 10 sayings'),
        ('write_20_sayings', 'Write 20 sayings'),
        ('write_30_sayings', 'Write 30 sayings'),
        ('write_40_sayings', 'Write 40 sayings'),

        ('write_10_sentences', 'Write 10 sentences'),
        ('write_20_sentences', 'Write 20 sentences'),
        ('write_30_sentences', 'Write 30 sentences'),
        ('write_40_sentences', 'Write 40 sentences'),

        ('report', 'Report bad content'),
)

class MileStoneType(models.Model):

    milestone_name = models.CharField(_("Name"), max_length=255, blank=False, null=True)
    milestone_type = models.CharField(_("Type"), max_length=255, choices=TYPE_CHOICES)
    milestone_desc = models.CharField(_("Description"), max_length=255, blank=False, null=True)
    milestone_pic = models.ImageField(
        _("Milestone picture"), upload_to='milestone/', max_length=None, blank=False, null=True)
    
    class Meta:
        verbose_name = _("MileStone type")
        verbose_name_plural = _("MileStone types")

class MileStone(models.Model):
    user = models.ForeignKey(
        "Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    milestone = models.ForeignKey(
        "MileStoneType", verbose_name=_("MileStone type"), on_delete=models.CASCADE)
    achievement_date = models.DateTimeField(
        _("Achievement date"), auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name = _("MileStone")
        verbose_name_plural = _("MileStones")