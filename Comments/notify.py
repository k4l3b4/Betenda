from betenda_api.methods import send_notification
from betenda_api.methods import save_notification

def comment_notification(instance, request, **kwargs):
    if not instance.parent:
        # It's a top level comment
        resource_type = instance.content_type.model.lower()
        if resource_type != "article":
            recipient = instance.content_object.user
        else:
            recipient = instance.content_object.authors.first()
        if recipient != instance.user:
            if resource_type == "article":
                notification = save_notification(user=recipient, message=f"Commented on your article!", type="3", comment=instance,  sender=instance.user, article=instance.content_object)
                send_notification(recipient.id, notification, request)

            elif resource_type=="saying":
                notification = save_notification(user=recipient, message=f"Commented on your saying!", type="3", comment=instance,  sender=instance.user, saying=instance.content_object)
                send_notification(recipient.id, notification, request)
            else:
                notification = save_notification(user=recipient, message=f"Commented on your poem!", type="3", comment=instance,  sender=instance.user, saying=instance.content_object)
                send_notification(recipient.id, notification, request)
    else:
        # It's a reply

        resource_type = instance.parent.content_type.model.lower()
        
        recipient = instance.immediate_parent.user
        if recipient != instance.user:
            if resource_type == "article":
                notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, article=instance.parent.content_object, comment=instance)
                send_notification(recipient.id, notification, request)
            
            elif resource_type=="saying":
                notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, saying=instance.parent.content_object, comment=instance)
                send_notification(recipient.id, notification, request)
            else:
                notification = save_notification(user=recipient, message=f"Replied to your comment!", type="3", sender=instance.user, poem=instance.parent.content_object, comment=instance)
                send_notification(recipient.id, notification, request)
