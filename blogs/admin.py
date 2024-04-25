from django.contrib import admin
from blogs.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'active']
    list_filter = ['active']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)