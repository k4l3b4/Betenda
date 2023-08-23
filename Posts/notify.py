from betenda_api.methods import send_notification, save_notification

def reply_to_comment_notification(instance, post,  request, **kwargs):
    recipient = instance.parent.user
    if recipient != instance.user:
        notification = save_notification(user=recipient, message=f"Replied to your post!", type="4", reply=instance, post=post,  sender=instance.user)
        send_notification(recipient.id, notification, request)