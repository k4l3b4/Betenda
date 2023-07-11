from django.contrib import admin

from .models import Comments

# Register your models here.


@admin.register(Comments)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "comment",
        "created_at",
        )
