from django.test import TestCase
from django.contrib.auth import get_user_model

from user.models import UserFollow
from core.constants.mock_data import john_doe, mock_user

tom_smith = mock_user(name="Tom Smith")
adam_jones = mock_user(name="Adam Jones")
ava_louise = mock_user(name="Ava Louise")


def create_user(**params):
    # Helper function to create a user.
    return get_user_model().objects.create_user(**params)


def create_user_follow(follower, following):
    # Helper function to create a user follow.
    return UserFollow.objects.create(follower=follower, following=following)


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


class UserFollowModelTests(TestCase):
    """Tests for UserFollow model."""

    def setUp(self):
        """Set up test dependencies."""
        self.user1 = create_user(**john_doe)
        self.user2 = create_user(**tom_smith)
        self.user3 = create_user(**adam_jones)
        self.user4 = create_user(**ava_louise)

    def test_create_user_follow(self):
        """Test creating a new user follow."""
        UserFollow.add_follower(self.user1, self.user2)

        # ! Fix
        self.assertTrue(UserFollow.is_following(self.user1, self.user2))
        self.assertFalse(UserFollow.is_following(self.user2, self.user1))

    def test_create_user_follow_with_invalid_credentials(self):
        """Test creating a new user follow with invalid credentials."""
        with self.assertRaises(ValueError):
            UserFollow.add_follower(self.user1, self.user1)
        with self.assertRaises(ValueError):
            UserFollow.add_follower(self.user1, None)
        with self.assertRaises(ValueError):
            UserFollow.add_follower(None, self.user1)
        with self.assertRaises(ValueError):
            UserFollow.add_follower("user1", self.user1)
        with self.assertRaises(ValueError):
            UserFollow.add_follower(self.user1, "user1")
        with self.assertRaises(ValueError):
            user_follow = UserFollow(follower=self.user1, following=self.user1)
            UserFollow.add_follower(user_follow, self.user1)

    def test_remove_user_follow(self):
        """Test removing a user follow."""
        UserFollow.add_follower(self.user1, self.user2)
        UserFollow.remove_follower(self.user1, self.user2)

        self.assertFalse(UserFollow.is_following(self.user1, self.user2))

    def test_remove_user_follow_with_invalid_credentials(self):
        """Test removing a user follow with invalid credentials."""
        with self.assertRaises(ValueError):
            UserFollow.remove_follower(self.user1, self.user1)
        with self.assertRaises(ValueError):
            UserFollow.remove_follower(self.user1, None)
        with self.assertRaises(ValueError):
            UserFollow.remove_follower(None, self.user1)
        with self.assertRaises(ValueError):
            UserFollow.remove_follower("user1", self.user1)
        with self.assertRaises(ValueError):
            UserFollow.remove_follower(self.user1, "user1")
        with self.assertRaises(ValueError):
            user_follow = UserFollow(follower=self.user1, following=self.user1)
            UserFollow.remove_follower(user_follow, self.user1)

    def test_get_followers(self):
        """Test getting a list of followers."""
        UserFollow.add_follower(self.user2, self.user1)
        UserFollow.add_follower(self.user3, self.user1)
        UserFollow.add_follower(self.user4, self.user1)

        followers = UserFollow.get_followers(self.user1)

        self.assertEqual(len(followers), 3)
        self.assertIn(self.user2, followers)
        self.assertIn(self.user3, followers)
        self.assertIn(self.user4, followers)

    def test_get_followers_with_invalid_credentials(self):
        """Test getting a list of followers with invalid credentials."""
        with self.assertRaises(ValueError):
            UserFollow.get_followers(None)
        with self.assertRaises(ValueError):
            UserFollow.get_followers("user1")

    def test_get_following(self):
        """Test getting a list of following."""
        UserFollow.add_follower(self.user1, self.user2)
        UserFollow.add_follower(self.user1, self.user3)
        UserFollow.add_follower(self.user1, self.user4)

        following = UserFollow.get_following(self.user1)

        self.assertEqual(len(following), 3)
        self.assertIn(self.user2, following)
        self.assertIn(self.user3, following)
        self.assertIn(self.user4, following)

    def test_get_following_with_invalid_credentials(self):
        """Test getting a list of following with invalid credentials."""
        with self.assertRaises(ValueError):
            UserFollow.get_following(None)
        with self.assertRaises(ValueError):
            UserFollow.get_following("user1")
