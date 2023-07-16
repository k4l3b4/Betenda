from django.contrib import admin

from .models import Comment

# Register your models here.


@admin.register(Comment)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "comment",
        "created_at",
        "updated_at",
        )
