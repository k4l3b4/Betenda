from rest_framework import generics
from betenda_api.methods import ServerError
from betenda_api.pagination import StandardResultsSetPagination
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.


class Notification_GET_View(generics.ListAPIView):
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

                # then replace the addition logic in the for loop with this:
                #  unread_count[notification.message_type] += 1


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