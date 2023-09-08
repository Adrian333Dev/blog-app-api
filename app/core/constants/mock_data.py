import random

from .constants import names


def random_salt():
    return str(random.randrange(100, 1000))


def mock_user(**kwargs):
    # Helper function to create a mock user.

    salt = kwargs.get("salt", random_salt())
    name = kwargs.get("name", random.choice(names))
    first_name, last_name = name.split(" ")

    return {
        "name": name,
        "username": f"{first_name.lower()}.{last_name.lower()}.{salt}",
        "email": f"{first_name.lower()}{last_name.lower()}{salt}@example.com",
        "password": f"pass_{reversed(first_name.lower())}{reversed(last_name.lower())}{salt}",
    }


# Mock Users

john_doe = mock_user(name="John Doe", salt="123")
