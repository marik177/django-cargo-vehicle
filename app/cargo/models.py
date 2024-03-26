from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_unique_vehicle_number


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"


class Cargo(models.Model):
    pick_up = models.ForeignKey(
        Location, related_name="pick_up_cargos", on_delete=models.CASCADE
    )
    delivery = models.ForeignKey(
        Location, related_name="delivery_cargos", on_delete=models.CASCADE
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    description = models.TextField()

    def __str__(self):
        return f"Cargo from {self.pick_up} to {self.delivery}"


class Vehicle(models.Model):
    unique_number = models.CharField(
        unique=True, validators=[validate_unique_vehicle_number]
    )
    current_location = models.ForeignKey(
        Location, related_name="vehicles", on_delete=models.CASCADE
    )
    carrying_capacity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )

    def __str__(self):
        return f"Vehicle {self.unique_number}"
