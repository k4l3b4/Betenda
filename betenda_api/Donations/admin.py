from django.contrib import admin

from Donations.models import Campaign

# Register your models here.


@admin.register(Campaign)
class Admin(admin.ModelAdmin):
    list_display = (
        "reason",
        "amount_needed",
        "amount_donated",
        "campaign_start",
        "campaign_end",
    )
