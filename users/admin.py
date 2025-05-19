from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff', 'is_active')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'followers_count', 'following_count', 'projects_count', 'publications_count')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('followers_count', 'following_count', 'projects_count', 'publications_count')

    def followers_count(self, obj):
        return obj.followers_count
    followers_count.short_description = 'Followers'

    def following_count(self, obj):
        return obj.following_count
    following_count.short_description = 'Following'

    def projects_count(self, obj):
        return obj.projects_count
    projects_count.short_description = 'Projects'

    def publications_count(self, obj):
        return obj.publications_count
    publications_count.short_description = 'Publications'


admin.site.register(CustomUser, CustomUserAdmin)
