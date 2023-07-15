from django.contrib import admin

from RoadMaps.models import Goal

# Register your models here.


@admin.register(Goal)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "goal_name",
        "goal_desc",
        "achieved",
        "canceled",
        "goal_set",
        "goal_due",
    )
