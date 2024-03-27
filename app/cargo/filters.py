from rest_framework import filters


class CargoWeightFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        weight_min = request.query_params.get("weight_min")
        weight_max = request.query_params.get("weight_max")

        if weight_min:
            queryset = queryset.filter(weight__gte=weight_min)

        if weight_max:
            queryset = queryset.filter(weight__lte=weight_max)

        return queryset
