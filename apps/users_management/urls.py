from dj_rest_auth.views import (
    LogoutView,
)
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users_management.views.user_login import CustomLoginView
from apps.users_management.views.user_registration import CustomRegisterView
from apps.users_management.views.user_view import (
    user_update,
    check_unique_username,
    check_unique_email,
    user_information, TestMail,
)

route = routers.DefaultRouter()
# route.register("users", UserViewSet)
urlpatterns = [
    path("", include(route.urls)),
    # user auth
    path("login/", CustomLoginView.as_view(), name='login'),
    path("register/", CustomRegisterView.as_view()),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # user basic apis
    path("user_update/<int:user_id>/", user_update),
    path("check_unique_username/", check_unique_username),
    path("check_unique_email/", check_unique_email),
    path("current-user/", user_information, name="current-user"),
    path("test_mail/", TestMail.as_view(), name="test_mail"),
]
