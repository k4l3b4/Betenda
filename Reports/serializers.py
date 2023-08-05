from Reports.models import Report
from rest_framework import serializers


class Report_Create_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['report','report_type']
    def create(self, validated_data):
        return super().create(validated_data)

class Report_GET_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'report',
            'report_type', 
            'user', 
            'created_at',
            'content_type',
            'object_id'
            ]