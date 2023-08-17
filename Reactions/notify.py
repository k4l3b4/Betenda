from betenda_api.methods import send_notification
from betenda_api.methods import save_notification

def reactions_notification(instance, request, content_object, **kwargs):
    resource_type = instance.content_type.model.lower()
    resource = instance.content_object

    if resource_type == "comment":
        resource_owner_type = instance.content_object.content_type.model.lower()
        resource_owner = content_object.content_object
    else:
        resource_owner = content_object


    if resource_type != "article":
        recipient = instance.content_object.user
    else:
        recipient = instance.content_object.authors.first()
    if recipient != instance.user:
        if resource_type == "article":
            notification = save_notification(user=recipient, message=f"Reacted to your article: {instance.reaction}!", type="1", sender=instance.user, article=resource)
            send_notification(recipient.id, notification, request)
        elif resource_type=="comment":
            if resource_owner_type == "article":
                notification = save_notification(user=recipient, message=f"Reacted to your comment: {instance.reaction}!", type="1", sender=instance.user, comment=resource, article=resource_owner)
                send_notification(recipient.id, notification, request)
            if resource_owner_type == "poem":
                notification = save_notification(user=recipient, message=f"Reacted to your comment: {instance.reaction}!", type="1", sender=instance.user, comment=resource, poem=resource_owner)
                send_notification(recipient.id, notification, request)
            if resource_owner_type == "saying":
                notification = save_notification(user=recipient, message=f"Reacted to your comment: {instance.reaction}!", type="1", sender=instance.user, comment=resource, saying=resource_owner)
                send_notification(recipient.id, notification, request)
        elif resource_type=="poem":
            notification = save_notification(user=recipient, message=f"Reacted to your poem: {instance.reaction}!", type="1", sender=instance.user, poem=resource)
            send_notification(recipient.id, notification, request)
        elif resource_type=="post":
            notification = save_notification(user=recipient, message=f"Reacted to your post: {instance.reaction}!", type="1", sender=instance.user, post=resource)
            send_notification(recipient.id, notification, request)
        else:
            notification = save_notification(user=recipient, message=f"Reacted to your saying: {instance.reaction}!", type="1", sender=instance.user, saying=resource)
            send_notification(recipient.id, notification, request)
