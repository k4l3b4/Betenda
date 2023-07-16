from django.contrib import admin

from .models import MileStone, MileStoneType

# Register your models here.


@admin.register(MileStoneType)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "milestone_name",
        "milestone_type",
        )
    
@admin.register(MileStone)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "milestone",
        "achievement_date",
        )

