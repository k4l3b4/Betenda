from django.contrib import admin

from .models import Engagement, HashTag, UserHashtag

# Register your models here.


@admin.register(HashTag)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "created_date",
    )


@admin.register(UserHashtag)
class Admin(admin.ModelAdmin):
    list_display = (
        "user",
        "hashtag",
        "score",
        "subscribed_at",
        "updated_at",
    )

@admin.register(Engagement)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "date",
        "int_amount",
    )
