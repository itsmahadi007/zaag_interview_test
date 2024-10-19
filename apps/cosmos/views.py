from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.cosmos.filter import CosmosModelFilter
from apps.cosmos.models import CosmosModel
from apps.cosmos.serializer import CosmosModelSerializer
from backend.utils.pagination import CustomPagination


# Create your views here.
class CosmosModelViewSet(viewsets.ModelViewSet):
    queryset = CosmosModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CosmosModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CosmosModelFilter
    pagination_class = CustomPagination
