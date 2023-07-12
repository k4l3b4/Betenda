from django.contrib import admin

from .models import Post

# Register your models here.


@admin.register(Post)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "content",
        "created_at",
        "edited_at",
        )
