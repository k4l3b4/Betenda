from django.contrib import admin

from .models import Device, FollowerRequest, UserProfile, Invitation, Password_reset, User
from django.contrib.auth.models import Permission
# Register your models here.

@admin.register(Permission)
class Admin(admin.ModelAdmin):
    list_display = ("name","codename")

@admin.register(FollowerRequest)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "follower",
        "is_approved",
        "requested_at",
    )

@admin.register(UserProfile)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "followers_count",
        "following_count",
    )

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
        "expired",
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
