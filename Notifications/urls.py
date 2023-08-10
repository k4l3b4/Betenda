from django.urls import path
from .views import Notification_GR_View

urlpatterns = [
    path('list', Notification_GR_View.as_view({'get': 'get'}), name="list_notifications_view"),
    path('read', Notification_GR_View.as_view({'post': 'mark_as_read'}), name="mark_notifications_as_read_view")
]
