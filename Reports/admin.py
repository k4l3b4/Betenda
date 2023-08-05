from django.contrib import admin
from .models import Report

# Register your models here.

@admin.register(Report)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "report",
        "report_type",
        "created_at",
    )