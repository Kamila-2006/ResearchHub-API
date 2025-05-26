from rest_framework import serializers
from .models import Publication
from .models import Finding
from .models import Project
from users.models import CustomUser

class PublicationSerializer(serializers.ModelSerializer):
    author_ids = serializers.PrimaryKeyRelatedField(many=True, source='authors', queryset=CustomUser.objects.all())
    finding_ids = serializers.PrimaryKeyRelatedField(many=True, source='findings', queryset=Finding.objects.all())
    project_id = serializers.PrimaryKeyRelatedField(source='project', queryset=Project.objects.all())

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'abstract', 'author_ids', 'journal', 'conference',
            'publication_date', 'doi', 'url', 'status', 'project_id', 'finding_ids', 'tags'
        ]
