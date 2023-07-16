from django.contrib import admin

from .models import Engagement, HashTag

# Register your models here.


@admin.register(HashTag)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "created_date",
    )

@admin.register(Engagement)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "date",
        "duration",
        "int_amount",
    )
