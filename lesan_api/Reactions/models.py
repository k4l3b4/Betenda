from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

class Reaction(models.Model):
    REACTION_CHOICES = (
        ('Like', 'Like'),
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
        ('❤', 'Red heart'),
        ('💔', 'Broken heart'),
        ('🆘', 'SOS'),
        ('🙆🏾‍♂️', 'Man raising hand'),
        ('🙆🏾‍♀️', 'Woman raising hand'),
        ('💪🏾', 'Flexed biceps'),
        ('🙏🏾', 'Folded hands'),
    )
    
    user = models.ForeignKey("Users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    reaction = models.CharField(_("Reaction"), max_length=255, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(_("Created date"), auto_now_add=True)
    content_type = models.ForeignKey(ContentType, verbose_name=_("Content type"), on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_("Object id"))
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user.username} reacted with {self.reaction} on {self.content_object}'
    
    class Meta:
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")