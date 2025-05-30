# Generated by Django 4.2 on 2025-05-24 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import apps.users.user_manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('institution', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('position', models.CharField(blank=True, choices=[('professor', 'Professor'), ('associate_professor', 'Associate Professor'), ('assistant_professor', 'Assistant Professor'), ('postdoc', 'Postdoc'), ('phd_student', 'PhD Student'), ('masters_student', 'Masters Student'), ('researcher', 'Researcher'), ('lab_technician', 'Lab Technician'), ('other', 'Other')], max_length=100, null=True)),
                ('orcid_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('researcher', 'Researcher')], default='researcher', max_length=20)),
                ('citation_count', models.PositiveIntegerField(default=0)),
                ('h_index', models.PositiveIntegerField(default=0)),
                ('profile_url', models.URLField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', apps.users.user_manager.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, max_length=200, null=True)),
                ('research_interests', models.JSONField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('website', models.URLField(blank=True, null=True)),
                ('google_scholar', models.URLField(blank=True, null=True)),
                ('researchgate', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='users.userprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
