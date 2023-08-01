from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


class Reaction(models.Model):
    REACTION_CHOICES = (
        ('😍', 'Heart eyes'),
        ('🥰', 'Smiling face with hearts'),
        ('🤩', 'Star-struck'),
        ('🤗', 'Hugging face'),
        ('😂', 'Face with tears of joy'),
        ('🤣', 'Rolling on the floor laughing'),
        ('😅', 'Grinning face with sweat'),
        ('😁', 'Grinning face with smiling eyes'),
        ('🙄', 'Face with rolling eyes'),
        ('😏', 'Smirking face'),
        ('😴', 'Sleeping face'),
        ('😜', 'Winking face with tongue'),
        ('🤐', 'Zipper-mouth face'),
        ('😲', 'Astonished face'),
        ('😤', 'Face with steam from nose'),
        ('🤯', 'Exploding head'),
        ('😡', 'Pouting face'),
        ('😠', 'Angry face'),
        ('😵', 'Dizzy face'),
        ('😈', 'Smiling face with horns'),
        ('🙈', 'See-no-evil monkey'),
        ('🙊', 'Speak-no-evil monkey'),
        ('🙉', 'Hear-no-evil monkey'),
        ('👀', 'Eyes'),
        ('❤️', 'Red heart'),
        ('💔', 'Broken heart'),
        ('🆘', 'SOS'),
        ('🙆🏾‍♂️', 'Man raising hand'),
        ('🙆🏾‍♀️', 'Woman raising hand'),
        ('💪🏾', 'Flexed biceps'),
        ('🙏🏾', 'Folded hands'),
    )

    user = models.ForeignKey("Users.User", verbose_name=_(
        "User"), on_delete=models.CASCADE)
    reaction = models.CharField(
        _("Reaction"), max_length=255, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    content_type = models.ForeignKey(ContentType, verbose_name=_(
        "Content type"), on_delete=models.CASCADE, db_index=True)
    object_id = models.PositiveIntegerField(_("Object id"), db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user.user_name} reacted with {self.reaction}'

    class Meta:
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")
        unique_together = ('user', 'reaction',
                           'content_type', 'object_id')

    def save(self, *args, **kwargs):
        created = self.pk is None  # Check if it's a new reaction
        super().save(*args, **kwargs)

        if created:
            content_type = ContentType.objects.get_for_model(
                self.content_object)
            try:
                reaction_count = ReactionCount.objects.get(
                    reaction=self.reaction, content_type=content_type, object_id=self.object_id)
                reaction_count.count += 1
                reaction_count.save()
            except ReactionCount.DoesNotExist:
                ReactionCount.objects.create(
                    reaction=self.reaction, content_type=content_type, object_id=self.object_id, count=1)

    def delete(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self.content_object)
        try:
            reaction_count = ReactionCount.objects.get(
                reaction=self.reaction, content_type=content_type, object_id=self.object_id
            )
            if reaction_count.count <= 1:
                reaction_count.delete()
            else:
                reaction_count.count -= 1
                reaction_count.save()
        except ReactionCount.DoesNotExist:
            pass
        super().delete(*args, **kwargs)


class ReactionCount(models.Model):
    '''
    Table to store the count of reactions for perf reasons
    '''
    reaction = models.CharField(
        max_length=255, choices=Reaction.REACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.count} {self.reaction}(s)"
    
    class Meta:
        verbose_name = _("Reaction Count")
        verbose_name_plural = _("Reactions Counts")
        unique_together = ('reaction', 'content_type', 'object_id')
