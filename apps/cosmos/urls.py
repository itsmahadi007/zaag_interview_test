from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.cosmos.views import (
    DataModelViewSet,
    ResultsViewSet,
    RootSampleViewSet,
    SubSampleViewSet,
    TaxonomyViewSet,
)

router = DefaultRouter()
router.register(r'data-models', DataModelViewSet, basename='DataModelViewSet')
router.register(r'results', ResultsViewSet, basename='ResultsViewSet')
router.register(r'root-samples', RootSampleViewSet, basename='RootSampleViewSet')
router.register(r'sub-samples', SubSampleViewSet, basename='SubSampleViewSet')
router.register(r'taxonomy', TaxonomyViewSet, basename='TaxonomyViewSet')
urlpatterns = [
    path("", include(router.urls)),
]
