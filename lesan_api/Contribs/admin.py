from django.contrib import admin

from .models import Poem, Saying, Sentence, TargetLanguage, SourceLanguage, Word

# Register your models here.


@admin.register(SourceLanguage)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "language",
        "iso_code",
        "glottolog_code",
        "created_at",
        "edited_at",
    )


@admin.register(TargetLanguage)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "language",
        "iso_code",
        "glottolog_code",
        "created_at",
        "edited_at",
    )


@admin.register(Word)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "word",
        "source_language",
        "target_language",
        "created_at",
    )


@admin.register(Poem)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "language",
        "created_at",
        "edited_at",
    )


@admin.register(Saying)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "language",
        "created_at",
        "edited_at",
    )


@admin.register(Sentence)
class Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "sentence",
        "source_language",
        "target_language",
        "created_at",
    )
