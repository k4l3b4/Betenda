from django.db import models
from django.utils.translation import gettext as _


class HashTag(models.Model):
    tag = models.CharField(_("tag"), max_length=255, blank=False, null=True)
    created_date = models.DateTimeField(
        _("Created date"), auto_now=False, auto_now_add=True)