from django.contrib import admin
from .models import BookMark

# Register your models here.
@admin.register(BookMark)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "content_type",
        "object_id",
        "content_object",
        "added_date",
    )