from django.test import TestCase
from django.contrib.auth import get_user_model

from core.constants.mock_data import john_doe


def create_user(**params):
    # Helper function to create a user.
    return get_user_model().objects.create_user(**params)


class UserModelTests(TestCase):
    """Tests for User model."""

    def test_create_user_with_required_fields(self):
        """Test creating a new user with required fields."""
        user = create_user(**john_doe)

        self.assertEqual(user.email, john_doe["email"])
        self.assertEqual(user.username, john_doe["username"])
        self.assertTrue(user.check_password(john_doe["password"]))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser_with_required_fields(self):
        """Test creating a new superuser with required fields."""
        user = get_user_model().objects.create_superuser(
            email=john_doe["email"],
            username=john_doe["username"],
            password=john_doe["password"],
        )
        self.assertEqual(user.email, john_doe["email"])
        self.assertEqual(user.username, john_doe["username"])
        self.assertTrue(user.check_password(john_doe["password"]))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_with_invalid_credentials(self):
        """Test creating a new user with invalid email."""
        user1 = {**john_doe, "email": None}
        user2 = {**john_doe, "username": None}
        with self.assertRaises(ValueError):
            create_user(**user1)
        with self.assertRaises(ValueError):
            create_user(**user2)

    def test_update_user_profile(self):
        """Test updating user profile."""
        user = create_user(**john_doe)
        payload = {
            "first_name": "Bob",
            "last_name": "Smith",
            "bio": "I am a software engineer.",
            "website": "https://example.com",
            "location": "Washington, DC",
        }
        for key, value in payload.items():
            setattr(user, key, value)
        user.save()

        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertEqual(user.bio, payload["bio"])
        self.assertEqual(user.website, payload["website"])
        self.assertEqual(user.location, payload["location"])
