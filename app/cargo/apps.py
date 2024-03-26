from django.apps import AppConfig


class CargoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cargo"

    def ready(self):
        from django.core.management import call_command

        # call_command("import_uszips", "cargo/data/uszips1.csv")
