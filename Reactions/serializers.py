
from Reactions.models import Reaction
from rest_framework import serializers


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['reaction']

    def create(self, validated_data):
        return super().create(validated_data)
