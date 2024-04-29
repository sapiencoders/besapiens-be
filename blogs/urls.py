from django.urls import path
from blogs.views import CategoryApiView, PostApiView, CommentApiView, preview_html_page

urlpatterns = [
    path('categories/', CategoryApiView.as_view()),
    path('posts/', PostApiView.as_view()),
    path('comments/', CommentApiView.as_view()),
    path('preview-html/<int:post_id>/', preview_html_page, name='preview_html'),
]
