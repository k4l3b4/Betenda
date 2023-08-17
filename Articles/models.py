import re
from django.db import models
from django.utils.translation import gettext as _
from HashTags.models import HashTag
from django_extensions.db.fields import AutoSlugField
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class Article(models.Model):
    STATUS = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    )

    title = models.CharField(
        _("Article title"), max_length=255, blank=False, db_index=True)
    slug = AutoSlugField(_("Slug"), populate_from=['title'])
    desc = models.CharField(_("Article description"),
                            max_length=255, blank=False, db_index=True)
    body = models.TextField(_("Article body"), blank=False)
    image = models.ImageField(
        _("Article image"), upload_to='article/images/', max_length=None, blank=True, null=True)
    thumbnail = models.ImageField(
        _("Image thumbnail"), upload_to='article/images/thumbnails/', max_length=None, blank=True, null=True)
    hashtags = models.ManyToManyField(
        "HashTags.HashTag", blank=True, db_index=True)
    authors = models.ManyToManyField("Users.User", verbose_name=_("Authors"), blank=True)
    status = models.CharField(_("Status"), choices=STATUS, max_length=255)
    featured = models.BooleanField(_("Featured"), default=False)
    published_date = models.DateTimeField(
        _("Published date"), auto_now=False, auto_now_add=True)
    report = GenericRelation("Reports.Report")
    bookmark = GenericRelation("BookMarks.Bookmark")
    modified_date = models.DateTimeField(
        _("modified date"), auto_now=True, auto_now_add=False)
    reactions = GenericRelation("Reactions.Reaction")
    comments = GenericRelation("Comments.Comment")

    def __str__(self):
        return f"{self.title[:20]}.., by {self.authors.first()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Run the async function
        self.process_hashtags()

    # async function to avoid blocking the system
    def process_hashtags(self):
        existing_hashtags = self.hashtags.all()

        # Extract hashtags from body
        hashtags = re.findall(r'#\w+', self.body)

        # remove tags that have been edited out
        for existing_tag in existing_hashtags:
            if existing_tag.tag[1:] not in hashtags:
                self.hashtags.remove(existing_tag)

        # Remove the '#' symbol from the tag
        for tag_text in hashtags:
            tag_name = tag_text[1:]

            # Check if the tag already exists
            existing_tag = existing_hashtags.filter(tag=tag_name).first()

            if not existing_tag:
                # Get or create the hashtag
                hashtag, _ = HashTag.objects.get_or_create(tag=tag_name)

                # Associate the hashtag with the post
                self.hashtags.add(hashtag)