from django_filters import rest_framework as filters
from django.db.models import Q

from apps.cosmos.models import DataModel


class DataModellFilter(filters.FilterSet):
    id = filters.CharFilter(method="filter")
    tax_id = filters.CharFilter(method="filter")
    name = filters.CharFilter(method="filter")
    relative_abundance_range = filters.CharFilter(method="filter")
    file_name = filters.CharFilter(method="filter")
    
    result_of = filters.CharFilter(method="filter")
    taxonomy = filters.CharFilter(method="filter")
    root_sample = filters.CharFilter(method="filter")
    sub_sample = filters.CharFilter(method="filter")

    class Meta:
        model = DataModel
        fields = [
            "primary_key",
            "tax_id",
            "id",
            "name",
            "relative_abundance_range",
            "file_name",
            "result_of",
            "taxonomy",
            "root_sample",
            "sub_sample",
        ]

    @staticmethod
    def filter(queryset, name, value):
        if name == "tax_id":
            return queryset.filter(tax_id=value)
        elif name == "id":
            return queryset.filter(id=value)
        elif name == "name":
            return queryset.filter(name__icontains=value)
        elif name == "result_of":
            return queryset.filter(result_of_id=value)
        elif name == "taxonomy":
            return queryset.filter(taxonomy_id=value)
        elif name == "root_sample":
            query = Q(result_of__sub_sample__root_sample_id=value) | Q(taxonomy__result_of__sub_sample__root_sample_id=value)
            return queryset.filter(query)
        elif name == "sub_sample":
            query = Q(result_of__sub_sample_id=value) | Q(taxonomy__result_of__sub_sample_id=value)
            return queryset.filter(query)
        elif name == "relative_abundance_range":
            try:
                min_value, max_value = [float(v.strip()) for v in value.split(",")]
                return queryset.filter(relative_abundance__range=(min_value, max_value))
            except ValueError:
                return queryset.none()
        elif name == "file_name":
            return queryset.filter(file_name__icontains=value)
        else:
            return queryset
