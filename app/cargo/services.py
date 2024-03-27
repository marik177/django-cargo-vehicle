from cargo.models import Location, Cargo


def create_cargo(validated_data):
    pick_up_properties = validated_data.pop("pick_up")
    zip_code = validated_data.pop("delivery").get("zip_code")

    # Filter pick_up location based on pick_up data
    pick_up_location = Location.objects.filter(
        **{key: value for key, value in pick_up_properties.items() if value is not None}
    ).first()

    # Get the delivery location based on zip_code
    delivery_location = Location.objects.get(zip_code=zip_code)

    validated_data["pick_up"] = pick_up_location
    validated_data["delivery"] = delivery_location

    return Cargo.objects.create(**validated_data)
