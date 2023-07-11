from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Article(models.Model):
    title = models.CharField(
        _("Article title"), max_length=150, blank=False, null=True)
    slug = models.SlugField(
        _("Article slug"), default="", blank=False, null=False)
    desc = models.CharField(_("Article description"),
                            max_length=255, blank=False, null=True)
    body = models.TextField(_("Article body"), blank=False, null=True)
    image = models.ImageField(
        _("Article image"), upload_to='article/images/', max_length=None, blank=True, null=True)
    authors = models.ManyToManyField("Users.User", verbose_name=_("Authors"))
    published_date = models.DateTimeField(
        _("Published date"), auto_now=False, auto_now_add=True)
    modified_date = models.DateTimeField(
        _("modified date"), auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return f"{self.title[:20]}.., by {self.authors.first()}"