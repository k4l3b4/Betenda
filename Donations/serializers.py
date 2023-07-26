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
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation

        fields = [
            "user",
            "donation_amount",
            "donation_for",
            "remark",
            "donation_date",
        ]

        extra_kwargs = {
            'user' : {'read_only':True},
            'donation_date' : {'read_only':True},
        }

    def create(self, validated_data):
        return super().create(validated_data)