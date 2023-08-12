from django.db import models
from django.utils.translation import gettext as _


class Notification(models.Model):
    TYPES = (
            ("1", 'Like'),
            ("2", 'Follow'),
            ("3", 'Comment'),
            ("4", 'Reply'),
            ("5", 'Liked-Comment'),
            ("6", 'Liked-Reply'), 
            ("7", 'System')
        )
    
    sender = models.ForeignKey('Users.User', verbose_name=_("Sender"), related_name='from_user', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey('Users.User', verbose_name=_("Recipient"), related_name='to_user', on_delete=models.CASCADE)
    post = models.ForeignKey('Posts.Post', related_name='notifiable_post', blank=True, null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey('Articles.Article', related_name='notifiable_article', blank=True, null=True, on_delete=models.SET_NULL)
    poem = models.ForeignKey('Contributions.Poem', related_name='notifiable_article', blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey('Comments.Comment', related_name='notifiable_article', blank=True, null=True, on_delete=models.SET_NULL)
    message = models.TextField(_("Message"))
    message_type = models.CharField(
        _("Message type"), choices=TYPES, default="7", max_length=50)
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
        ordering=('-created_at',)