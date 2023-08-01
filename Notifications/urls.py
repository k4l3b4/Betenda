from django.urls import path
from .views import Notification_GET_View

urlpatterns = [
    path('list', Notification_GET_View.as_view(), name="list_notifications_view")
]
