from rest_framework import serializers
from .models import Finding

class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = ['id',
                  'title',
                  'description',
                  'data_summary',
                  'conclusion',
                  'significance',
                  'visibility',
                  'experiment',
        ]