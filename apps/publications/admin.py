from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'publication_date', 'project')
    list_filter = ('status', 'publication_date', 'project')
    search_fields = ('title', 'abstract', 'doi')
    filter_horizontal = ('authors', 'findings')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
