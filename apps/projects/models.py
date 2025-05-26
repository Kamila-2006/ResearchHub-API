from django.db import models
from apps.groups.models import Group
from apps.users.models import CustomUser
from apps.core.models import BaseModel


class Tag(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Project(BaseModel):
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
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='planning')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    funding_source = models.CharField(max_length=300, null=True, blank=True)
    funding_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    funding_currency = models.CharField(max_length=10, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    principal_investigator = models.ForeignKey('users.CustomUser', related_name='led_projects', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class ProjectMember(BaseModel):
    ROLE_CHOICES = [
        ('principal_investigator', 'Principal Investigator'),
        ('co_investigator', 'Co-Investigator'),
        ('research_assistant', 'Research Assistant'),
        ('collaborator', 'Collaborator'),
        ('observer', 'Observer'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        unique_together = ('project', 'user')
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.title} ({self.role})"
