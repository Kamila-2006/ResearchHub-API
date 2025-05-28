from django.contrib import admin
from .models import Finding

@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ('title', 'significance', 'visibility', 'experiment')
    list_filter = ('significance', 'visibility')
    search_fields = ('title', 'description', 'data_summary', 'conclusion')
