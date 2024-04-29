from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import safe
from blogs.models import Category, Post, Comment
from blogs.serializers import CategorySerializer, PostSerializer, CommentSerializer

# Create your views here.


class CategoryApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        stuffs = Category.objects.all()
        serializer = CategorySerializer(stuffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        stuffs = Post.objects.all()
        serializer = PostSerializer(stuffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentApiView(APIView):
    # 1. List all
    def get(self, request, *args, **kwargs):
        stuffs = Comment.objects.all()
        serializer = CommentSerializer(stuffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def preview_html_page(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.content:
        return HttpResponse(safe(get_themed_content(post.content)), content_type='text/html')
    return HttpResponse("No content available for preview")


def get_themed_content(content):
    return f"""
      <meta charset="UTF-8">
      <div style="height: 300px; border-bottom: 2px solid black;"></div>
      <div style="position: relative; margin-left: 400px; width: 700px;">
        {content}
      </div>
    """
