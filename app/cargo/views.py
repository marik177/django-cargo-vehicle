from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from .filters import CargoWeightFilter
from .models import Cargo
from .serializers import (
    CargoCreateSerializer,
    CargoReadSerializer,
    CargoEditSerializer,
    CargoWithVehiclesDistanceSerializer,
)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    filter_backends = [CargoWeightFilter]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            if "max_distance_miles" in self.request.query_params:
                return CargoWithVehiclesDistanceSerializer
            return CargoReadSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return CargoEditSerializer
        else:
            return CargoCreateSerializer
