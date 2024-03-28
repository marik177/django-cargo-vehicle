from random import choice
import logging

from celery import shared_task
from cargo.models import Vehicle, Location
from cargo.services import get_locations, get_vehicles, update_vehicles


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def update_vehicle_locations(self):
    # Get all locations
    all_locations = list(get_locations())
    vehicles = []
    # Iterate through all vehicles
    for vehicle in get_vehicles():
        # Select a random location
        new_location = choice(all_locations)

        # Update the vehicle's current location
        vehicle.current_location = new_location
        vehicles.append(vehicle)
    try:
        update_vehicles(vehicles)
        logger.info("Vehicle current locations updated")
        return "Vehicle current locations updated"
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise self.retry(exc=e)
