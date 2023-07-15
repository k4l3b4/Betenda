from django.db import models
from django.utils.translation import gettext as _


class Notification(models.Model):
    user = models.ForeignKey('Users.User', verbose_name=_(
        "User"), on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    is_read = models.BooleanField(_("Is read"), default=False)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"{self.message[15]}... Read: {self.is_read}"

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")