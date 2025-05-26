from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField
from apps.core.models import BaseModel
from .user_manager import CustomUserManager


class CustomUser(AbstractUser, BaseModel):
    POSITION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('postdoc', 'Postdoc'),
        ('phd_student', 'PhD Student'),
        ('masters_student', 'Masters Student'),
        ('researcher', 'Researcher'),
        ('lab_technician', 'Lab Technician'),
        ('other', 'Other'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('researcher', 'Researcher'),
    ]
    objects = CustomUserManager()

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institution = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, blank=True, null=True)
    orcid_id = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='researcher')
    citation_count = models.PositiveIntegerField(default=0)
    h_index = models.PositiveIntegerField(default=0)
    profile_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=200, blank=True, null=True)
    research_interests = JSONField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    google_scholar = models.URLField(blank=True, null=True)
    researchgate = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)


    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def projects_count(self):
        return self.project_set.count()

    @property
    def publications_count(self):
        return self.publication_set.count()

    @property
    def projects(self):
        from apps.projects import Project
        return Project.objects.filter(members__user=self.user).distinct()

    def __str__(self):
        return f"{self.user.email} Profile"



