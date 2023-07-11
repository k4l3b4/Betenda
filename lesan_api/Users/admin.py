from django.contrib import admin

from .models import Device, Invitation, Password_reset, User

# Register your models here.


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "user_name",
        "phone_number",
        "is_active",
        "is_superuser",
    )

@admin.register(Invitation)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "invitation_code",
        "disabled",
        "count",
    )

@admin.register(Password_reset)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "otp",
        "created_at",
        "expires_at",
    )

@admin.register(Device)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "ip_address",
        "device_type",
        "city",
        "country",
        "logged_in",
    )
