from django.db import models
from apps.core.models import BaseModel
from apps.projects.models import Tag
from apps.experiments.models import Experiment

class Finding(BaseModel):
    SIGNIFICANCE_CHOICES = [
        ('breakthrough', 'Breakthrough'),
        ('important', 'Important'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    data_summary = models.TextField()
    conclusion = models.TextField()
    significance = models.CharField(max_length=20, choices=SIGNIFICANCE_CHOICES)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='findings')
    tags = models.ManyToManyField(Tag, blank=True, related_name='findings')

    def __str__(self):
        return self.title