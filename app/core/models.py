# Database models for the application.

# class Post(Model):
#     """
#     Post model represents individual articles or posts published on your platform.
#     Stores post content, metadata, and statistics.
#     Includes fields for title, content, author, timestamps, likes, comments, tags, etc.
#     """

#     # Content
#     title = CharField(max_length=255)
#     excerpt = TextField(blank=True, null=True)
#     content = TextField()

#     # Author
#     author = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE, related_name="posts")

#     # Timestamps
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)

#     # Metadata
#     slug = AutoSlugField(populate_from="title", unique=True)
#     is_published = BooleanField(default=False)
#     published_at = DateTimeField(null=True, blank=True)
#     cover_image = ImageField(upload_to=post_cover_image_path, null=True, blank=True)

#     # Stats
#     views = PositiveIntegerField(default=0)

#     # Tags
#     tags = ManyToManyField("Tag", related_name="posts", blank=True)

#     # Relationships
#     reactions = ManyToManyField("Reaction", related_name="post_reactions", blank=True)

#     def __str__(self):
#         """Return the string representation of the post."""
#         return f"{self.id} - {self.title}"


# class Comment(Model):
#     """
#     Comment model represents comments made on posts.
#     Stores comment content, author, and timestamps.
#     May include fields for replies and reactions (emojis).
#     """

#     # Content
#     content = TextField()

#     # Author
#     author = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)

#     # Timestamps
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)

#     # Relationships
#     post = ForeignKey(Post, on_delete=CASCADE)
#     parent = ForeignKey("self", on_delete=CASCADE, null=True, blank=True)
#     reactions = ManyToManyField("Reaction", related_name="comment_reactions")

#     # Metadata
#     deleted = BooleanField(default=False)
#     deleted_at = DateTimeField(null=True, blank=True)

#     def __str__(self):
#         """Return the string representation of the comment."""
#         return f"{self.id} - {self.content}"


# class Tag(Model):
#     """
#     Tag model represents tags or categories assigned to posts.
#     Stores tag names and related metadata.
#     """

#     # Metadata
#     name = SlugField(max_length=255, unique=True, db_index=True)
#     description = TextField(blank=True)
#     image = ImageField(upload_to=tag_image_path, null=True, blank=True)

#     # Timestamps
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)

#     # Stats
#     popularity_score = IntegerField(default=0)  # Based on post usage
#     usage_count = IntegerField(default=0)  # Number of posts using the tag

#     def __str__(self):
#         """Return the string representation of the tag."""
#         return f"{self.id} - {self.name}"


# class Reaction(Model):
#     """
#     Reaction model represents user reactions to posts or comments.
#     Stores information about the user, post/comment being reacted to, and the type of reaction (e.g., like, emoji).
#     """

#     user = ForeignKey(User, on_delete=SET_NULL, null=True, db_index=True)
#     post = ForeignKey(Post, on_delete=SET_NULL, null=True, blank=True)
#     reaction_type = ForeignKey("ReactionType", on_delete=SET_NULL, null=True)

#     class Meta:
#         unique_together = ["user", "post", "reaction_type"]

#     def __str__(self):
#         """Return the string representation of the reaction."""
#         return f"{self.id} - {self.user} - {self.post} - {self.reaction_type}"


# class ReactionType(Model):
#     """
#     ReactionType model represents reaction types.
#     Stores information about the reaction type (e.g., like, emoji).
#     """

#     label = CharField(max_length=255, unique=True)
#     emoji = CharField(max_length=255, unique=True)  # Unicode emoji

#     def __str__(self):
#         """Return the string representation of the reaction type."""
#         return f"{self.id} - {self.label}"


# class Bookmark(Model):
#     """
#     Represents bookmarks made by users to save posts.
#     Stores information about the user and the saved post.
#     """

#     user = ForeignKey(User, on_delete=CASCADE)
#     post = ForeignKey(Post, on_delete=CASCADE)
#     notes = TextField(blank=True)

#     created_at = DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ["user", "post"]
#         ordering = ["-created_at"]

#     def __str__(self):
#         """Return the string representation of the bookmark."""
#         return f"{self.post.title} - {self.user.username}"
