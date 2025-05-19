from django.db import models
from groups.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=100)
    short_description = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='planning')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    funding_source = models.CharField(max_length=300)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2)
    funding_currency = models.CharField(max_length=10)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    #tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title



class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('principal_investigator', 'Principal Investigator'),
        ('co_investigator', 'Co-Investigator'),
        ('research_assistant', 'Research Assistant'),
        ('collaborator', 'Collaborator'),
        ('observer', 'Observer'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.title} ({self.role})"