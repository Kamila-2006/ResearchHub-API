from django.contrib import admin
from .models import Project, ProjectMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'visibility', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'description', 'short_description')


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role', 'joined_at', 'is_active')
    list_filter = ('role', 'is_active')
