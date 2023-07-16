from RoadMaps.models import Goal
from rest_framework import serializers
from rest_framework.fields import MaxLengthValidator


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id",
            "goal_name",
            "goal_desc",
            "achieved",
            "goal_set",
            "goal_due",
            "canceled",
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'goal_desc': {'validators': [MaxLengthValidator(700)]},
            'canceled': {'read_only': True},
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
