from rest_framework import serializers
from django.conf import settings
from .models import Location, Cargo, Vehicle
from .services import (
    create_cargo,
    cargo_update,
    find_vehicles_within_distance_from_cargo,
)


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


class CargoReadSerializer(serializers.ModelSerializer):
    pick_up = LocationPickUpSerializer()
    delivery = LocationPickUpSerializer()
    number_of_vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = [
            "id",
            "pick_up",
            "delivery",
            "description",
            "weight",
            "number_of_vehicles",
        ]

    def get_number_of_vehicles(self, obj):
        cargo_id = obj.id
        vehicles_within_distance = find_vehicles_within_distance_from_cargo(cargo_id)
        return len(vehicles_within_distance)


class CargoWithVehiclesDistanceSerializer(CargoReadSerializer):
    nearest_vehicles_distance = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = [
            "id",
            "pick_up",
            "delivery",
            "description",
            "weight",
            "number_of_vehicles",
            "nearest_vehicles_distance",
        ]

    def get_nearest_vehicles_distance(self, obj):
        max_distance_miles = self.context["request"].query_params.get(
            "max_distance_miles"
        )
        nearest_vehicles_distance = find_vehicles_within_distance_from_cargo(
            obj.id, max_distance_miles
        )
        return [distance for vehicle_number, distance in nearest_vehicles_distance]


class CargoCreateSerializer(serializers.ModelSerializer):
    pick_up = LocationPickUpSerializer()
    delivery = LocationDeliverySerializer()

    class Meta:
        model = Cargo
        fields = ["id", "pick_up", "delivery", "weight", "description"]

    def create(self, validated_data):
        return create_cargo(validated_data)


class CargoEditSerializer(serializers.Serializer):
    weight = serializers.IntegerField()
    description = serializers.CharField()

    def update(self, instance, validated_data):
        return cargo_update(instance, validated_data)


class CargoDetailSerializer(CargoReadSerializer):
    nearest_vehicles = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = [
            "id",
            "pick_up",
            "delivery",
            "description",
            "weight",
            "number_of_vehicles",
            "nearest_vehicles",
        ]

    def get_nearest_vehicles(self, obj):
        nearest_vehicles = find_vehicles_within_distance_from_cargo(
            obj.id, settings.MAX_DELIVERY_DISTANCE
        )
        return nearest_vehicles


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
