from rest_framework.views import APIView
from Donations.models import Campaign
from Donations.serializers import CampaignSerializer


class Campaign_CU_View(APIView):
    serializer_class = CampaignSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
