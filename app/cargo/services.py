from operator import itemgetter
from random import choice

from cargo.models import Location, Cargo, Vehicle
from geopy.distance import geodesic
from rest_framework.exceptions import ValidationError


def create_cargo(validated_data):
    pick_up_properties = validated_data.pop("pick_up")
    zip_code = validated_data.pop("delivery").get("zip_code")

    # Filter pick_up location based on pick_up data
    pick_up_location = Location.objects.filter(
        **{key: value for key, value in pick_up_properties.items() if value is not None}
    ).first()

    # Check if pick_up_location is None
    if not pick_up_location:
        raise ValidationError(
            "Pick-up location with the given parameters does not exist"
        )

    # Get the delivery location based on zip_code
    delivery_location = Location.objects.filter(zip_code=zip_code).first()

    # Check if delivery_location is None
    if not delivery_location:
        raise ValidationError(
            "Delivery location with the given zip code does not exist"
        )

    validated_data["pick_up"] = pick_up_location
    validated_data["delivery"] = delivery_location

    return Cargo.objects.create(**validated_data)


def cargo_update(instance, validated_data):
    # Update the instance with the validated data
    instance.weight = validated_data.get("weight", instance.weight)
    instance.description = validated_data.get("description", instance.description)
    instance.save()
    return instance


def find_vehicles_within_distance_from_cargo(cargo_id, max_distance_miles=450):
    # Get the cargo's pick-up location
    cargo = Cargo.objects.get(id=cargo_id)
    pick_up_location = cargo.pick_up

    # Get the latitude and longitude of the cargo's pick-up location
    cargo_coords = (pick_up_location.latitude, pick_up_location.longitude)

    # Query vehicles and calculate distances
    vehicle_distances = []
    all_vehicles = Vehicle.objects.all()
    for vehicle in all_vehicles:
        vehicle_coords = (
            vehicle.current_location.latitude,
            vehicle.current_location.longitude,
        )
        distance = geodesic(cargo_coords, vehicle_coords).miles
        if distance <= float(max_distance_miles):
            vehicle_distances.append((vehicle, distance))

    # Sort vehicles by distance (nearest first)
    sorted_vehicles = sorted(vehicle_distances, key=itemgetter(1))
    return [
        (vehicle.unique_number, round(distance, 2))
        for vehicle, distance in sorted_vehicles
    ]


class UpdateVehicleLocationService:
    def __init__(self):
        self.vehicles = []

    @staticmethod
    def _extract_all_locations():
        return list(Location.objects.all())

    @staticmethod
    def _extract_all_vehicles():
        return Vehicle.objects.all()

    def _add_location(self):
        all_locations = self._extract_all_locations()
        all_vehicles = self._extract_all_vehicles()
        for vehicle in all_vehicles:
            # Select a random location
            new_location = choice(all_locations)
            # Update the vehicle's current location
            vehicle.current_location = new_location
            self.vehicles.append(vehicle)

    def _update_locations(self):
        Vehicle.objects.bulk_update(self.vehicles, ["current_location"])

    def execute(self):
        self._add_location()
        self._update_locations()
