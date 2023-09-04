import yaml


def yaml_coerce(value):
    # Coerce a string representation of a dict to a dict.

    if isinstance(value, str):
        try:
            return yaml.safe_load(value)
        except yaml.YAMLError as exc:
            raise ValueError(exc)
    else:
        return value
