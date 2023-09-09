# Database models for the application.

import uuid
import os

from django.conf import settings
from django.db.models import (
    Model,
    CharField,
    TextField,
    IntegerField,
    PositiveIntegerField,
    EmailField,
    BooleanField,
    DateTimeField,
    SlugField,
    ImageField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
    SET_NULL,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# from django.utils import timezone

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


def post_cover_image_path(instance, filename):
    return image_path(filename, "post_cover_images")


def tag_image_path(instance, filename):
    return image_path(filename, "tag_images")


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

    username = CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from="username", unique=True)
    email = EmailField(max_length=255, unique=True)
    first_name = CharField(max_length=100, blank=True)
    last_name = CharField(max_length=100, blank=True)
    bio = TextField(blank=True)
    location = CharField(max_length=255, blank=True)
    avatar = ImageField(upload_to=user_avatar_path, null=True, blank=True)
    cover_image = ImageField(upload_to=user_cover_image_path, null=True, blank=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(auto_now_add=True)

    # required fields: username, email, password

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

    follower = ForeignKey(User, on_delete=CASCADE, related_name="following")
    following = ForeignKey(User, on_delete=CASCADE, related_name="followers")

    class Meta:
        unique_together = ["follower", "following"]

    def __str__(self):
        """Return the string representation of the user-follow relationship."""
        return (
            f"Follower: {self.follower.username} - Following: {self.following.username}"
        )

    def save(self, *args, **kwargs):
        """Override save method to prevent users from following themselves."""
        if self.follower == self.following:
            raise ValueError("Users cannot follow themselves.")
        super().save(*args, **kwargs)

    @classmethod
    def add_follower(cls, follower, following):
        """Add a follower to a user."""
        user_follow = cls(follower=follower, following=following)
        user_follow.save()

    @classmethod
    def remove_follower(cls, follower, following):
        """Remove a follower from a user."""
        cls.objects.filter(follower=follower, following=following).delete()


class Post(Model):
    """
    Post model represents individual articles or posts published on your platform.
    Stores post content, metadata, and statistics.
    Includes fields for title, content, author, timestamps, likes, comments, tags, etc.
    """

    # Content
    title = CharField(max_length=255)
    excerpt = TextField(blank=True, null=True)
    content = TextField()

    # Author
    author = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name="posts")

    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Metadata
    slug = AutoSlugField(populate_from="title", unique=True)
    is_published = BooleanField(default=False)
    published_at = DateTimeField(null=True, blank=True)
    cover_image = ImageField(upload_to=post_cover_image_path, null=True, blank=True)

    # Stats
    views = PositiveIntegerField(default=0)

    # Tags
    tags = ManyToManyField("Tag", related_name="posts", blank=True)

    # Relationships
    reactions = ManyToManyField("Reaction", related_name="post_reactions", blank=True)

    def __str__(self):
        """Return the string representation of the post."""
        return f"{self.id} - {self.title}"


class Comment(Model):
    """
    Comment model represents comments made on posts.
    Stores comment content, author, and timestamps.
    May include fields for replies and reactions (emojis).
    """

    # Content
    content = TextField()

    # Author
    author = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)

    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Relationships
    post = ForeignKey(Post, on_delete=CASCADE)
    # ! Consider using this: parent = ManyToManyField("self", blank=True)
    parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True)
    reactions = ManyToManyField("Reaction", related_name="comment_reactions")

    # Metadata
    deleted = BooleanField(default=False)
    deleted_at = DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return the string representation of the comment."""
        return f"{self.id} - {self.content}"


class Tag(Model):
    """
    Tag model represents tags or categories assigned to posts.
    Stores tag names and related metadata.
    """

    # Metadata
    name = SlugField(max_length=255, unique=True, db_index=True)
    description = TextField(blank=True)
    image = ImageField(upload_to=tag_image_path, null=True, blank=True)

    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # Stats
    popularity_score = IntegerField(default=0)  # Based on post usage
    usage_count = IntegerField(default=0)  # Number of posts using the tag

    def __str__(self):
        """Return the string representation of the tag."""
        return f"{self.id} - {self.name}"


class TagFollow(Model):
    """
    TagFollow model represents user-following relationships for tags.
    Stores information about the follower and the tag being followed.
    """

    follower = ForeignKey(User, on_delete=CASCADE, related_name="tag_following")
    tag = ForeignKey(Tag, on_delete=CASCADE, related_name="tag_followers")

    class Meta:
        unique_together = ["follower", "tag"]

    def __str__(self):
        """Return the string representation of the tag-follow relationship."""
        return f"Follower: {self.follower.username} - Tag: {self.tag.name}"

    def save(self, *args, **kwargs):
        """Override save method to prevent users from following tags they are already following."""
        if self.follower == self.tag:
            raise ValueError("Users cannot follow tags they are already following.")
        super().save(*args, **kwargs)

    @classmethod
    def add_follower(cls, follower, tag):
        """Add a follower to a tag."""
        tag_follow = cls(follower=follower, tag=tag)
        tag_follow.save()

    @classmethod
    def remove_follower(cls, follower, tag):
        """Remove a follower from a tag."""
        cls.objects.filter(follower=follower, tag=tag).delete()


class Reaction(Model):
    """
    Reaction model represents user reactions to posts or comments.
    Stores information about the user, post/comment being reacted to, and the type of reaction (e.g., like, emoji).
    """

    user = ForeignKey(User, on_delete=SET_NULL, null=True, db_index=True)
    post = ForeignKey(Post, on_delete=SET_NULL, null=True, blank=True)
    reaction_type = ForeignKey("ReactionType", on_delete=SET_NULL, null=True)

    class Meta:
        unique_together = ["user", "post", "reaction_type"]

    def __str__(self):
        """Return the string representation of the reaction."""
        return f"{self.id} - {self.user} - {self.post} - {self.reaction_type}"


class ReactionType(Model):
    """
    ReactionType model represents reaction types.
    Stores information about the reaction type (e.g., like, emoji).
    """

    label = CharField(max_length=255, unique=True)
    emoji = CharField(max_length=255, unique=True)  # Unicode emoji

    def __str__(self):
        """Return the string representation of the reaction type."""
        return f"{self.id} - {self.label}"


class Bookmark(Model):
    """
    Represents bookmarks made by users to save posts.
    Stores information about the user and the saved post.
    """

    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)
    notes = TextField(blank=True)

    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]
        ordering = ["-created_at"]

    def __str__(self):
        """Return the string representation of the bookmark."""
        return f"{self.post.title} - {self.user.username}"


"""
Other optional models to add:
UserBlock

Notification
- Represents notifications sent to users for various events (e.g., new followers, likes, comments).
- Stores notification content, recipient, and timestamps.

Badge
Represents badges or achievements earned by users.
Stores badge names and related metadata.

ActivityLog
Logs user activity and actions on the platform.
Stores information about the user, the type of action, and timestamps.
Useful for auditing and analytics.

Message
Represents direct messages or private messages between users.
Stores message content, sender, recipient, and timestamps.
May include fields for read status and message threading.
"""
