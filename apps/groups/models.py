from django.db import models
from users.models import CustomUser
from core.models import BaseModel


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Member(BaseModel):
    ROLE_CHOICES = (
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('assistant', 'Assistant'),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.role}) - {self.group.name}"