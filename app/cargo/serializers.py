from rest_framework import serializers
from .models import Location, Cargo, Vehicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["zip_code"]


class CargoSerializer(serializers.ModelSerializer):
    delivery = LocationSerializer()

    class Meta:
        model = Cargo
        fields = ["id", "pick_up", "delivery", "weight", "description"]

    def create(self, validated_data):
        zip_code = validated_data.pop("delivery").get("zip_code")
        delivery_location = Location.objects.get(zip_code=zip_code)
        validated_data["delivery"] = delivery_location
        print(validated_data)
        return "qwerty"


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
