from django.contrib import admin
from blogs.models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'display_categories',
        'created_at',
        'active',
    ]
    list_filter = ['active']
    search_fields = ['title']

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'notes', 'created_at']
    search_fields = ['name']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
