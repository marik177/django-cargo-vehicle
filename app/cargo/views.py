from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from .filters import CargoWeightFilter
from .models import Cargo
from .serializers import CargoCreateSerializer, CargoReadSerializer, CargoEditSerializer


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    filter_backends = [CargoWeightFilter]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CargoReadSerializer
        elif self.request.method == "PUT" or self.request.method == "PATCH":
            return CargoEditSerializer
        else:
            return CargoCreateSerializer
