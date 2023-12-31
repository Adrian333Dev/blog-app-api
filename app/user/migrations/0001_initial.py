# Generated by Django 4.0.10 on 2023-09-10 21:53

import autoslug.fields
from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='username', unique=True)),
                ('email', models.EmailField(db_index=True, help_text='Required. 255 characters or fewer. Must be a valid email address.', max_length=255, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=user.models.user_avatar_path)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to=user.models.user_cover_image_path)),
                ('website', models.CharField(blank=True, max_length=255)),
                ('twitter', models.CharField(blank=True, max_length=255)),
                ('github', models.CharField(blank=True, max_length=255)),
                ('linkedin', models.CharField(blank=True, max_length=255)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
    ]
