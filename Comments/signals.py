from django.db.models.signals import post_save
from django.dispatch import receiver
from Comments.models import Comment
from betenda_api.methods import send_notification
from betenda_api.methods import save_notification

@receiver(post_save, sender=Comment)
def create_send_notification_for_comment_or_reply(sender, instance, created, **kwargs):
    if created:
        # Check if it's a top-level comment or reply
        if not instance.parent:
            # It's a top level comment
            resource_type = instance.content_type.model.lower()
            if resource_type == "article":
                recipient = instance.content_object.authors.first()
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Commented on your article!", type="3", sender=instance.user, article=instance.content_object)
                    send_notification(recipient.id, notification)
                pass

            elif resource_type=="saying":
                recipient = instance.content_object.user
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Commented on your saying!", type="3", sender=instance.user, saying=instance.content_object)
                    send_notification(recipient.id, notification)
                pass
            else:
                recipient = instance.content_object.user
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Commented on your poem!", type="3", sender=instance.user, saying=instance.content_object)
                    send_notification(recipient.id, notification)
                pass

        else:
            # It's a reply
            resource_type = instance.parent.content_type.model.lower()
            if resource_type == "article":
                recipient = instance.content_object.authors.first()
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, article=instance.parent.content_object, comment=instance.parent)
                    send_notification(recipient.id, notification)
                pass
            
            elif resource_type=="saying":
                recipient = instance.parent.user
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, saying=instance.parent.content_object, comment=instance.parent)
                    send_notification(recipient.id, notification)
                pass
            else:
                recipient = instance.parent.user
                if recipient != instance.user:
                    notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, poem=instance.parent.content_object, comment=instance.parent)
                    send_notification(recipient.id, notification)
                pass