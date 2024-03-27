from rest_framework import serializers
from .models import Location, Cargo, Vehicle
from .services import create_cargo


class LocationDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["zip_code"]


class LocationPickUpSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, allow_null=True)
    state = serializers.CharField(max_length=100, allow_null=True)
    zip_code = serializers.CharField(max_length=20, allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)


class CargoSerializer(serializers.ModelSerializer):
    pick_up = LocationPickUpSerializer()
    delivery = LocationDeliverySerializer()

    class Meta:
        model = Cargo
        fields = ["id", "pick_up", "delivery", "weight", "description"]

    def create(self, validated_data):
        return create_cargo(validated_data)


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
