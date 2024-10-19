from rest_framework import serializers

from apps.cosmos.models import CosmosModel


class CosmosModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CosmosModel
        fields = "__all__"
