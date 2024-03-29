from operator import itemgetter
from random import choice
from dataclasses import dataclass

from cargo.models import Location, Cargo, Vehicle
from geopy.distance import geodesic
from rest_framework.exceptions import ValidationError


@dataclass
class VehicleDistanceRow:
    unique_number: str
    distance: float


class UpdateVehicleLocationService:
    def __init__(self):
        self.vehicles = []

    def _get_all_locations():
        return list(Location.objects.all())

    def _get_all_vehicles():
        return Vehicle.objects.all()

    def _add_location(self):
        all_locations = self._get_all_locations()
        all_vehicles = self._get_all_vehicles()
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


class VehicleFinderService:
    def __init__(self, cargo_id, max_distance_miles=450):
        self.cargo_id = cargo_id
        self.max_distance_miles = max_distance_miles
        self.number_of_vehicles = None

    def execute(self):
        # Get the cargo object
        cargo = self._get_cargo()
        # Get the vehicle objects
        all_vehicles = self._get_all_vehicles()
        vehicle_distances = self._calculate_vehicle_distances(cargo, all_vehicles)
        return sorted(vehicle_distances, key=lambda x: x.distance)

    def _get_cargo(self):
        return Cargo.objects.get(id=self.cargo_id)

    def _get_all_vehicles(self):
        return Vehicle.objects.all()

    def _calculate_vehicle_distances(self, cargo, vehicles):
        cargo_coords = (cargo.pick_up.latitude, cargo.pick_up.longitude)
        vehicle_distances = []
        for vehicle in vehicles:
            vehicle_coords = (
                vehicle.current_location.latitude,
                vehicle.current_location.longitude,
            )
            distance = geodesic(cargo_coords, vehicle_coords).miles
            if distance <= float(self.max_distance_miles):
                vehicle_distances.append(
                    VehicleDistanceRow(
                        unique_number=vehicle.unique_number, distance=round(distance, 2)
                    )
                )
        self.number_of_vehicles = len(vehicle_distances)
        return vehicle_distances


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
