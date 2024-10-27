from dj_rest_auth.views import LoginView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users_management.serializers.basic_users_serializer import UserSerializerShort


class CustomLoginView(LoginView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        data = self.get_response()
        user = self.user
        user_serializer = UserSerializerShort(user, context={"request": request})

        access_token = data.data["access"]
        refresh_token = data.data["refresh"]
        data = {
            "access": access_token,
            "refresh": refresh_token,
            "user": user_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
