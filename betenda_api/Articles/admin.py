from django.contrib import admin
from Articles.models import Article

# Register your models here.


@admin.register(Article)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "featured",
        "published_date",
        "modified_date",
        )