import os

from .misc import yaml_coerce


def get_settings_from_env(prefix: str = "APP_") -> dict:
    """Get settings from environment variables.

    Args:
        prefix (str): Prefix for environment variables.

    Returns:
        dict: Settings dictionary.
    """
    prefix_len = len(prefix)
    settings = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            settings[key[prefix_len:]] = yaml_coerce(value)
    # print(settings)
    # print(prefix)
    return settings
