from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.cosmos.filter import DataModellFilter
from apps.cosmos.models import DataModel, Results, RootSample, SubSample, Taxonomy
from apps.cosmos.serializer import DataModelSerializer, DataModelDetailsSerializer, ResultsDetailsReverseSerializer, ResultsSerializer, RootSampleDetailsSerializer, RootSampleSerializer, SubSampleDetailsReverseSerializer, SubSampleSerializer, TaxonomyDetailsSerializer, TaxonomySerializer
from backend.utils.pagination import CustomPagination


# Create your views here.
class DataModelViewSet(viewsets.ModelViewSet):
    queryset = DataModel.objects.all().order_by('primary_key')
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = DataModellFilter
    pagination_class = CustomPagination

    serializer_classes = {
        "list": DataModelDetailsSerializer,
        "retrieve": DataModelDetailsSerializer,
        "create": DataModelSerializer,
        "update": DataModelSerializer,
    }

    default_serializer_class = DataModelDetailsSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    serializer_classes = {
        "list": TaxonomyDetailsSerializer,
        "retrieve": TaxonomyDetailsSerializer,
        "create": TaxonomySerializer,
        "update": TaxonomySerializer,
    }

    default_serializer_class = TaxonomyDetailsSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    serializer_classes = {
        "list": ResultsDetailsReverseSerializer,
        "retrieve": ResultsDetailsReverseSerializer,
        "create": ResultsSerializer,
        "update": ResultsSerializer,
    }

    default_serializer_class = ResultsDetailsReverseSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class SubSampleViewSet(viewsets.ModelViewSet):
    queryset = SubSample.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    serializer_classes = {
        "list": SubSampleDetailsReverseSerializer,
        "retrieve": SubSampleDetailsReverseSerializer,
        "create": SubSampleSerializer,
        "update": SubSampleSerializer,
    }

    default_serializer_class = SubSampleDetailsReverseSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class RootSampleViewSet(viewsets.ModelViewSet):
    queryset = RootSample.objects.all().order_by('id')
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    serializer_classes = {
        "list": RootSampleDetailsSerializer,
        "retrieve": RootSampleDetailsSerializer,
        "create": RootSampleSerializer,
        "update": RootSampleSerializer,
    }

    default_serializer_class = RootSampleDetailsSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
