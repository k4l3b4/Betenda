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
        from Reactions.methods import update_reaction_count
        created = not self.pk  # Check if the instance is being created or updated
        id = self.pk
        object_id = self.object_id
        previous_reaction = None
        if not created:
            try:
                previous_reaction = Reaction.objects.get(pk=id)
            except Reaction.DoesNotExist:
                pass

        # You should replace 'self.reaction', 'self.content_type', and 'self.object_id'
        # with the actual values corresponding to the reaction being saved.
        content_type = ContentType.objects.get_for_model(
                        self.content_object)

        # Call the function to update the reaction count.
        update_reaction_count(created, previous_reaction, self.reaction, content_type, object_id)

        super(Reaction, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
        # created = self.pk is None  # Check if it's a new reaction
        # if not created:
        #     try:
        #         previous_reaction = Reaction.objects.get(id=self.pk)
        #     except:
        #         previous_reaction = None

        # super().save(*args, **kwargs)
        # content_type = ContentType.objects.get_for_model(
        #         self.content_object)
        # if created:
        #     try:
        #         reaction_count = ReactionCount.objects.get(
        #             reaction=self.reaction, content_type=content_type, object_id=self.object_id)
        #         reaction_count.count += 1
        #         reaction_count.save()
        #     except ReactionCount.DoesNotExist:
        #         ReactionCount.objects.create(
        #             reaction=self.reaction, content_type=content_type, object_id=self.object_id, count=1)
        # else:
        #     try:
        #         old_reaction_count = ReactionCount.objects.get(
        #             reaction=previous_reaction.reaction, content_type=content_type, object_id=previous_reaction.object_id
        #         )
        #         if old_reaction_count.count <= 1:
        #             old_reaction_count.delete()
        #         else:
        #             old_reaction_count.count -= 1
        #             old_reaction_count.save()

        #         try:
        #             reaction_count = ReactionCount.objects.get(
        #                 reaction=self.reaction, content_type=content_type, object_id=self.object_id)
        #             reaction_count.count += 1
        #             reaction_count.save()
        #         except ReactionCount.DoesNotExist:
        #             ReactionCount.objects.create(
        #                 reaction=self.reaction, content_type=content_type, object_id=self.object_id, count=1)
                    
        #     except ReactionCount.DoesNotExist:
        #         ReactionCount.objects.create(
        #             reaction=self.reaction, content_type=content_type, object_id=self.object_id, count=1)


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
