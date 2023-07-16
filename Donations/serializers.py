from rest_framework import serializers

from Donations.models import Campaign, Donation


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "reason",
            "amount_needed",
            "amount_donated",
            "campaign_start",
            "campaign_end",
        ]


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            "donation_amount",
            "donation_for",
            "remark",
            "donation_date",
        ]
