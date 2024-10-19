from django_filters import rest_framework as filters

from apps.cosmos.models import CosmosModel


class CosmosModelFilter(filters.FilterSet):
    tax_id = filters.CharFilter(method="filter")
    name = filters.CharFilter(method="filter")
    relative_abundance_range = filters.CharFilter(method="filter")
    file_name = filters.CharFilter(method="filter")

    class Meta:
        model = CosmosModel
        fields = [
            "tax_id",
            "name",
            "relative_abundance_range",
            "file_name"
        ]

    @staticmethod
    def filter(queryset, name, value):
        if name == "tax_id":
            return queryset.filter(tax_id=value)
        elif name == "name":
            return queryset.filter(name__icontains=value)
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
