from django.contrib import admin

from .models import Reaction, ReactionCount

# Register your models here.


@admin.register(Reaction)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "reaction",
        "content_type",
        "created_at",
        )
    
@admin.register(ReactionCount)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "reaction",
        "count",
        "object_id",
        "content_type",
        )
