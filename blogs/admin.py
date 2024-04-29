from django.contrib import admin
from django.utils.html import format_html
from blogs.models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'display_categories',
        'created_at',
        'active',
        'preview_html_link',
    ]
    list_filter = ['active']
    search_fields = ['title']

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'

    def preview_html_link(self, obj):
        if obj.content:
            # Constructing the URL directly
            preview_url = f'/api/preview-html/{obj.id}/'
            return format_html('<a href="{}" target="_blank">Preview HTML</a>', preview_url)
        return '-'
    preview_html_link.short_description = 'Preview HTML'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'notes', 'created_at']
    search_fields = ['name']


class PostsFilter(admin.SimpleListFilter):
    title = "Posts"
    parameter_name = "post"

    def lookups(self, request, model_admin):
        q = Post.objects.filter()
        return tuple((s.id, s) for s in q)

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        if queryset.model == Comment:
            return queryset.filter(post__id=value)
        return queryset


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'comment',
        'parent_comment',
        'post',
        'created_at',
        'active',
    ]
    search_fields = ['name', 'email']
    list_filter = ['active', PostsFilter]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
