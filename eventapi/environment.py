import os

environment = os.environ.get("ENVIRONMENT", "LOCAL")


def get_settings():
    if environment == "LOCAL":
        return "eventapi.settings.local"
    elif environment == "STAGING":
        return "eventapi.settings.staging"
