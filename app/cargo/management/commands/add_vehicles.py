import random
from string import ascii_uppercase

from django.core.management.base import BaseCommand
from cargo.models import Vehicle, Location


class Command(BaseCommand):
    help = "Populates the database with initial vehicle entries"

    def handle(self, *args, **kwargs):
        # Get all location IDs from the database
        location_ids = list(Location.objects.values_list("id", flat=True))

        for i in range(1, 21):
            unique_number = str(random.randint(1000, 9999)) + random.choice(
                ascii_uppercase
            )
            carrying_capacity = random.randint(1, 1000)
            # Randomly select a location ID from the available ones
            current_location_id = random.choice(location_ids)
            Vehicle.objects.create(
                unique_number=unique_number,
                current_location_id=current_location_id,
                carrying_capacity=carrying_capacity,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with initial vehicle entries."
            )
        )
