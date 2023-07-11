from django.contrib import admin

from .models import Reaction

# Register your models here.


@admin.register(Reaction)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "reaction",
        "created_at",
        )
