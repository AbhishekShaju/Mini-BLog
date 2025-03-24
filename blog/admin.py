from django.contrib import admin
from .models import Post, Profile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'is_draft', 'is_deleted')
    list_filter = ('is_draft', 'is_deleted', 'date_posted')
    search_fields = ('title', 'content')
    ordering = ('-date_posted',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'bio')
