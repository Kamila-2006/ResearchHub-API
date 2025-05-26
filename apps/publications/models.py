from django.db import models
from apps.projects import Project
from apps.findings import Finding
from apps.users.models import CustomUser


class Publication(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    abstract = models.TextField()
    journal = models.CharField(max_length=200, blank=True, null=True)
    conference = models.CharField(max_length=200, blank=True, null=True)
    publication_date = models.DateField()
    doi = models.CharField(max_length=200)
    url = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    authors = models.ManyToManyField(CustomUser)
    findings = models.ManyToManyField(Finding)
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.title