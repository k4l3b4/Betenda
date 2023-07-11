from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class SourceLanguage(models.Model):
    language = models.CharField(
        _("Language name"), max_length=50, blank=False, null=True)
    iso_code = models.CharField(
        _("Language ISO code"), max_length=10, blank=False, null=True)
    glottolog_code = models.CharField(
        _("Language Glottolog code"), max_length=10, blank=False, null=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.language}({self.code})"

    class Meta:
        verbose_name = _("Source Language")
        verbose_name_plural = _("Source Languages")


class TargetLanguage(models.Model):
    language = models.CharField(
        _("Language name"), max_length=50, blank=False, null=True)
    iso_code = models.CharField(
        _("Language ISO code"), max_length=10, blank=False, null=True)
    glottolog_code = models.CharField(
        _("Language Glottolog code"), max_length=10, blank=False, null=True)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.language}({self.code})"

    class Meta:
        verbose_name = _("Target Language")
        verbose_name_plural = _("Target Languages")


class Word(models.Model):
    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.SET_NULL, blank=False, null=True)
    word = models.CharField(_("Word"), max_length=255, blank=False, null=True)
    source_language = models.ForeignKey("SourceLanguage", verbose_name=_(
        "Source language"), related_name="word_source_language", on_delete=models.PROTECT)
    target_language = models.ForeignKey("TargetLanguage", verbose_name=_(
        "Target language"), related_name="word_target_language", on_delete=models.PROTECT)
    synonym = models.ManyToManyField("self", verbose_name=_(
        "Synonym"))
    antonym = models.ManyToManyField("self", verbose_name=_(
        "Antonym"))
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.word}(source lang:{self.source_language}, target lang:{self.target_language})"

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")


class Poem(models.Model):
    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.SET_NULL, blank=False, null=True)
    poem = models.TextField(_("Poem"), blank=False, null=True)
    language = models.ForeignKey("TargetLanguage", related_name="poem_language", verbose_name=_(
        "Language"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.poem[:20]}({self.language})"

    class Meta:
        verbose_name = _("Poem")
        verbose_name_plural = _("Poems")


class Saying(models.Model):
    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.SET_NULL, blank=False, null=True)
    saying = models.TextField(_("Saying"), blank=False, null=True)
    language = models.ForeignKey("TargetLanguage", related_name="saying_language", verbose_name=_(
        "Language"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.saying[:20]}({self.language})"

    class Meta:
        verbose_name = _("Saying")
        verbose_name_plural = _("Sayings")


class Sentence(models.Model):
    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.SET_NULL, blank=False, null=True)
    sentence = models.TextField(_("Saying"), blank=False, null=True)
    source_language = models.ForeignKey("SourceLanguage", related_name="sentence_source_language", verbose_name=_(
        "Source language"), on_delete=models.PROTECT)
    target_language = models.ForeignKey("TargetLanguage", related_name="sentence_target_language", verbose_name=_(
        "Target language"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    edited_at = models.DateTimeField(_("Edited date"), blank=True, null=True)

    def __str__(self):
        return f"{self.sentence[:20]}(source lang:{self.source_language}, target lang:{self.target_language})"

    class Meta:
        verbose_name = _("Sentence")
        verbose_name_plural = _("Sentences")
