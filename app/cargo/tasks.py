from random import choice
import logging

from celery import shared_task

from cargo.services import UpdateVehicleLocationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def update_vehicle_locations(self):
    update_vehicle_service = UpdateVehicleLocationService()
    try:
        update_vehicle_service.execute()
        logger.info("Vehicle current locations updated")
        return "Vehicle current locations updated"
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise self.retry(exc=e)
