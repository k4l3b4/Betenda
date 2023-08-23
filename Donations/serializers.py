from rest_framework import serializers
from .models import CampaignShots, Campaign, Donation


class CampaignShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignShots
        fields = ('id', 'shot', 'description', 'type')
        extra_kwargs = {
            'id':{'read_only': True},
            'type':{'read_only': True}
        }

class CampaignSerializer(serializers.ModelSerializer):
    campaign_shots = CampaignShotsSerializer(many=True)

    class Meta:
        model = Campaign
        fields = [
            "reason",
            "amount_needed",
            "amount_donated",
            "campaign_start",
            "campaign_end",
            'campaign_shots',
        ]

    def create(self, validated_data):
        try:
          shots_data = validated_data.pop('shots')
        except:
          shots_data = None

        campaign = super().create(validated_data)

        if shots_data:
            for shot_data in shots_data:
                CampaignShots.objects.create(campaign=campaign, **shot_data)
        return campaign
    
    def update(self, instance, validated_data):
        shots_data = validated_data.pop('shots_data', [])

        instance.update(**validated_data)
        # Create new CampaignShots instances
        for shot_data in shots_data:
            CampaignShots.objects.create(campaign=instance, **shot_data)

        return instance
    


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