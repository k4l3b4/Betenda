from django.db.models.signals import post_save
from django.dispatch import receiver
from Reactions.models import Reaction
from betenda_api.methods import send_notification
from betenda_api.methods import save_notification

@receiver(post_save, sender=Reaction)
def create_send_notification_for_reactions(sender, instance, created, **kwargs):
    if created:
        resource_type = instance.content_type.model.lower()
        if resource_type != "article":
            recipient = instance.content_object.user
        else:
            recipient = instance.content_object.authors.first()
        if recipient != instance.user:
            if resource_type == "article":
                notification = save_notification(user=recipient, message=f"Reacted to your article: {instance.reaction}!", type="1", sender=instance.user, article=instance.content_object)
                send_notification(recipient.id, notification)
            elif resource_type=="comment":
                notification = save_notification(user=recipient, message=f"Reacted to your comment: {instance.reaction}!", type="1", sender=instance.user, comment=instance.content_object)
                send_notification(recipient.id, notification)
            elif resource_type=="poem":
                notification = save_notification(user=recipient, message=f"Reacted to your poem: {instance.reaction}!", type="1", sender=instance.user, poem=instance.content_object)
                send_notification(recipient.id, notification)
            elif resource_type=="post":
                notification = save_notification(user=recipient, message=f"Reacted to your post: {instance.reaction}!", type="1", sender=instance.user, post=instance.content_object)
                send_notification(recipient.id, notification)
            else:
                notification = save_notification(user=recipient, message=f"Reacted to your saying: {instance.reaction}!", type="1", sender=instance.user, saying=instance.content_object)
                send_notification(recipient.id, notification)
