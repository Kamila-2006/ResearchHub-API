from django.contrib import admin
from .models import Experiment

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date', 'project')
    list_filter = ('status', 'start_date', 'end_date', 'project')
    search_fields = ('title', 'description', 'hypothesis', 'methodology')
    filter_horizontal = ('collaborators',)

