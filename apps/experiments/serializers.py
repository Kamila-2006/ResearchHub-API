from rest_framework import serializers
from .models import Experiment
from users.serializers import UserProfileSerializer


class ExperimentSerializer(serializers.ModelSerializer):
    collaborators = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Experiment
        fields = [
            'id',
            'title',
            'description',
            'hypothesis',
            'methodology',
            'start_date',
            'end_date',
            'status',
            'project',
            'collaborators',
        ]
