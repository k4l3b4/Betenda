from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Goal(models.Model):
    GOAL_TYPE = (
        ('DEV', 'Development goal'),
        ('COM', 'Community goal'),
        ('GOYE', 'Civic goal'),
    )

    goal_name = models.CharField(_("Goal name"), max_length=255)
    goal_desc = models.TextField(_("Goal description"))
    goal_type = models.CharField(
        _("Goal type"), choices=GOAL_TYPE, max_length=255)
    achieved = models.BooleanField(_("Goal achieved"), default=False)
    goal_set = models.DateTimeField(
        _("Goal set on"), auto_now=False, auto_now_add=False)
    goal_due = models.DateTimeField(
        _("Ideal achievement date"), auto_now=False, auto_now_add=False)
    canceled = models.BooleanField(_("Goal canceled"), default=False)

    def __str__(self):
        return f"{self.goal_name} due on {self.goal_due}, achieved: {self.achieved}"
    
    class Meta:
        verbose_name=_("Goal")
        verbose_name_plural=_("Goals")

    def set_achieved(self):
        """
        Method to mark the goal as achieved.
        """
        self.achieved = True
        self.save()
    
    def set_canceled(self):
        """
        Method to mark the goal as canceled.
        """
        self.canceled = True
        self.save()