import random

from .constants import first_names, last_names


def random_salt():
    return str(random.randrange(100, 1000))


def mock_user(**kwargs):
    # Helper function to create a mock user.

    salt = kwargs.get("salt", random_salt())
    first_name, last_name = kwargs.get(
        "name", random.choice(first_names) + " " + random.choice(last_names)
    ).split(" ")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "username": f"{first_name.lower()}.{last_name.lower()}.{salt}",
        "email": f"{first_name.lower()}{last_name.lower()}{salt}@example.com",
        "password": f"pass_{reversed(first_name.lower())}{salt}{reversed(last_name.lower())}",
    }


# Mock Users
john_doe = mock_user(name="John Doe", salt="123")
