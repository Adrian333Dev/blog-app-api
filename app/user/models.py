import uuid
import os

from django.conf import settings
from django.db.models import (
    Model,
    UUIDField,
    CharField,
    TextField,
    EmailField,
    BooleanField,
    DateTimeField,
    ImageField,
    ForeignKey,
    CASCADE,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from autoslug import AutoSlugField


AUTH_USER_MODEL = settings.AUTH_USER_MODEL


def image_path(filename, folder):
    """Generate file path for new image."""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/", folder, filename)


def user_avatar_path(instance, filename):
    return image_path(filename, "avatars")


def user_cover_image_path(instance, filename):
    return image_path(filename, "cover_images")


class UserManager(BaseUserManager):
    """User manager for the application."""

    def create_user(self, email, username, password=None, **extra_fields):
        """Create a new user for the application."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Create a new superuser for the application."""
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        if not password:
            raise ValueError("Users must have a password.")

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model represents registered users of your platform.
    Stores user profile information, authentication data, and preferences.
    Includes fields for user stats, roles, and privacy settings.
    """

    # Info
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = CharField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[UnicodeUsernameValidator()],
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    slug = AutoSlugField(populate_from="username", unique=True)
    email = EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        validators=[validate_email],
        help_text="Required. 255 characters or fewer. Must be a valid email address.",
    )
    first_name = CharField(max_length=100, blank=True)
    last_name = CharField(max_length=100, blank=True)
    bio = TextField(blank=True)
    location = CharField(max_length=255, blank=True)
    date_joined = DateTimeField(auto_now_add=True)

    # Profile
    avatar = ImageField(upload_to=user_avatar_path, null=True, blank=True)
    cover_image = ImageField(upload_to=user_cover_image_path, null=True, blank=True)

    # Social
    website = CharField(max_length=255, blank=True)
    twitter = CharField(max_length=255, blank=True)
    github = CharField(max_length=255, blank=True)
    linkedin = CharField(max_length=255, blank=True)

    # Stats
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """Return the string representation of the user."""
        return self.email


class UserFollow(Model):
    """
    UserFollow model represents user-following relationships.
    Stores information about the follower and the user being followed.
    """

    follower = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name="following")
    following = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name="followers")

    class Meta:
        unique_together = ["follower", "following"]

    def __str__(self):
        """Return the string representation of the user-follow relationship."""
        return f"Follower: {self.follower} - Following: {self.following}"

    def save(self, *args, **kwargs):
        """Override save method to prevent users from following themselves."""
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves.")
        super().save(*args, **kwargs)

    @classmethod
    def add_follower(cls, following, follower):
        """Add a follower to the following."""
        if follower is None or following is None:
            raise ValueError("Follower and following entities cannot be None.")
        user_follow = cls(following=following, follower=follower)
        user_follow.save()

    @classmethod
    def remove_follower(cls, following, follower):
        """Remove a follower from the following."""
        if follower == following:
            raise ValueError("Users cannot unfollow themselves.")
        if follower is None or following is None:
            raise ValueError("Follower and following entities cannot be None.")
        cls.objects.filter(following=following, follower=follower).delete()

    @classmethod
    def get_followers(cls, following):
        """Get a list of followers for a following."""
        followers = cls.objects.filter(following=following)
        return [follower.follower for follower in followers]

    @classmethod
    def get_following(cls, follower):
        """Get a list of followings for a follower."""
        followings = cls.objects.filter(follower=follower)
        return [following.following for following in followings]

    @classmethod
    def is_following(cls, follower, following):
        """Check if a follower is following a following."""
        if follower is None or following is None:
            raise ValueError("Follower and following entities cannot be None.")
        return cls.objects.filter(follower=follower, following=following).exists()
