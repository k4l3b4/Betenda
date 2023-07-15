from django.contrib import admin

from Notifications.models import Notification

# Register your models here.


@admin.register(Notification)
class Admin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "is_read",
        "created_at",
    )
