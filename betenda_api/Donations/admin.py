from django.contrib import admin

from .models import Campaign, Donation

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

@admin.register(Donation)
class Admin(admin.ModelAdmin):
    list_display = (
        "user",
        "donation_amount",
        "donation_for",
        "remark",
        "donation_date",
        )