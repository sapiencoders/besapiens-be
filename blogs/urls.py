from django.urls import path
from blogs.serializers import CategoryApiView, PostApiView, CommentApiView

urlpatterns = [
    path('categories/', CategoryApiView.as_view()),
    path('posts/', PostApiView.as_view()),
    path('comments/', CommentApiView.as_view()),
]
