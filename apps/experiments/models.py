from django.db import models
from apps.users.models import CustomUser
from apps.projects.models import Project, Tag


class Experiment(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    hypothesis = models.TextField()
    methodology = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='experiments')
    collaborators = models.ManyToManyField(CustomUser, related_name='experiments')
    tags = models.ManyToManyField(Tag, related_name='experiments')

    def __str__(self):
        return self.title