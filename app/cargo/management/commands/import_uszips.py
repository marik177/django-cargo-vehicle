import csv
import os
from itertools import islice
from django.core.management.base import BaseCommand
from cargo.models import Location


class Command(BaseCommand):
    help = "Imports uszips.csv data into the PostgreSQL database"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str, help="The path to the CSV file")

    def handle(self, *args, **options):

        filename = options["filename"]

        if not os.path.exists(filename):
            self.stdout.write(self.style.ERROR(f'File "{filename}" not found.'))
            return

        with open(filename, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            locations = []
            for row in csv_reader:
                locations.append(
                    Location(
                        city=row["city"],
                        state=row["state_name"],
                        zip_code=row["zip"],
                        latitude=row["lat"],
                        longitude=row["lng"],
                    )
                )
            Location.objects.bulk_create(locations, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported data from "{filename}" into the database.'
            )
        )
