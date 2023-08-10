from betenda_api.methods import send_response
from rest_framework.decorators import action
from betenda_api.methods import mark_notification_as_read
from rest_framework import viewsets
from betenda_api.pagination import StandardResultsSetPagination
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.


class Notification_GR_View(viewsets.ModelViewSet):
    queryset = Notification.objects.all().select_related('user')
    serializer_class = NotificationSerializer

    def get_unread_count(self, notifications):
        unread_count = 0
        for notification in notifications:
            if not notification.is_read:
                unread_count += 1

        return unread_count
        # if you want to return the count type for every notification type:       
        #  # unread_count = {
                #     '1': 0,
                #     '2': 0,
                #     '3': 0,
                #     '4': 0,
                #     '5': 0,
                #     '6': 0,
                #     '7': 0,
                # }

                # then replace the addition logic in the for loop above with this:
                # unread_count[notification.message_type] += 1
                # i'd rather not do that

    @action(detail=True, methods=['get'])
    def get(self, request, *args, **kwargs):
        user = request.user
        notifications = self.queryset.filter(user=user)
        pagination_class = StandardResultsSetPagination()
        paginated_notifications = pagination_class.paginate_queryset(
            notifications, request)

        # Calculate the unread_count for the user
        unread_count = self.get_unread_count(notifications)

        # Combine unread_count with the serialized data
        serializer = self.serializer_class(paginated_notifications, many=True, context={'request': request})
        response_data = {
            'unread_count': unread_count,
            'notifications': serializer.data,
        }

        return pagination_class.get_paginated_response(response_data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, *args, **kwargs):
        ids_string = request.data.get('ids', None)
        ids = [int(id_str) for id_str in ids_string.split(',')]
        # Since our frontend is handling the updating optimistically 
        # there will be little use in returning an error if some notifications aren't marked as read
        mark_notification_as_read(ids)
        return send_response(None, "Notifications read successfully")