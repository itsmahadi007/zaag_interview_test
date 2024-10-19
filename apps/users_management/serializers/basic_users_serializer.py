from rest_framework import serializers

from apps.users_management.models import UserManage
from backend.utils.custom_attachchment_serializer import add_attachment_data


class UserSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_image",
            "profile_image_thumbnail",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = add_attachment_data(representation, instance, "profile_image")
        representation = add_attachment_data(
            representation, instance, "profile_image_thumbnail"
        )
        return representation


class UserSerializerExtraShort(serializers.ModelSerializer):
    class Meta:
        model = UserManage
        fields = (
            "id",
            "username",
            "email",
        )
