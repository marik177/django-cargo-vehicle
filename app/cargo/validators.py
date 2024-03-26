import re

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_unique_vehicle_number(value):
    if not re.match(r"^\d{4}[A-Z]$", value):
        raise ValidationError(
            _(
                "Unique number should be a digit from 1000 to 9999 followed by a capital English letter."
            ),
            code="invalid",
        )
