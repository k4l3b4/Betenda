from django.contrib import admin

from Notifications.models import Notification

# Register your models here.


@admin.register(Notification)
class Admin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "message_type",
        "is_read",
        "created_at",
    )
