from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from betenda_api.methods import BadRequest, send_response, ServerError
from betenda_api.pagination import StandardResultsSetPagination
from .models import Donation
from .serializers import DonationSerializer
from .serializers import CampaignSerializer


class Campaign_CU_View(APIView):
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminUser,]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response("Campaign added successfully", 201)
        except:
          return ServerError("There was an error on our side")
        
    def patch(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.serializer_class(data=data, partial=True)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response("Campaign updated successfully", 200)
        except:
          return ServerError("There was an error on our side")

class Donation_CR_View(APIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            notifications = self.queryset.filter(user=user)
            pagination_class = StandardResultsSetPagination()
            paginated_notifications = pagination_class.paginate_queryset(
                notifications, request)
            serializer = self.serializer_class(paginated_notifications, many=True)

            return pagination_class.get_paginated_response(serializer.data)
        except:
          return ServerError("There was an error on our side")
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                raise BadRequest(serializer.errors)
            serializer.save()
            return send_response("Thank you for your generous donation!", 201)
        except:
          return ServerError("There was an error on our side")