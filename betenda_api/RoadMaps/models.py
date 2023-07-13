from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class RoadMap(models.Model):
    goal_name = models.CharField(_("Goal name"), max_length=255)
    goal_desc = models.CharField(_("Goal description"), max_length=255)
    achieved = models.BooleanField(_("Goal achieved"), default=False)
    goal_set = models.DateTimeField(_("Goal set on"), auto_now=False, auto_now_add=True)
    goal_due = models.DateTimeField(_("Ideal achievement date"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.goal_name} due on {self.goal_due}, achieved: {self.achieved}"
    