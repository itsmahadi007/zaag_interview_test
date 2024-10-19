from django.urls import path, include
from rest_framework import routers

from apps.cosmos.views import CosmosModelViewSet

route = routers.DefaultRouter()
route.register("cosmos", CosmosModelViewSet, basename="CosmosModelViewSet")
urlpatterns = [
    path("", include(route.urls)),
]
