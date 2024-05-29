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
        title: str = kwargs.get('title')
        if title is not None:
            stuffs = Post.objects.filter(
                active=True, title=title.replace("-", " "))
        else:
            stuffs = Post.objects.filter(active=True)
        serializer = PostSerializer(stuffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentApiView(APIView):
    # 1. List all comments for a specific blog_id
    def get(self, request, *args, **kwargs):
        # Retrieve the blog_id from the request parameters
        post_id = kwargs.get('post_id')

        if post_id is not None:
            # Filter comments by the specific post_id
            comments = Comment.objects.filter(
                post__id=int(post_id), active=True)
        else:
            # If no post_id is provided, return all comments (optional)
            comments = Comment.objects.filter(active=True)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create a new comment
    def post(self, request, *args, **kwargs):
        data = request.data
        print(f'new comment: {data}')

        # Ensure 'name', 'email', 'post_id', and 'comment' are provided
        required_fields = ['name', 'email', 'post_id', 'comment']
        for field in required_fields:
            if field not in data:
                return Response({field: ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if the post_id exists
        post_id = data['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"post_id": ["Invalid post ID."]}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for creating the comment
        comment_data = {
            'name': data['name'],
            'email': data['email'],
            'comment': data['comment'],
            'post': post_id,
        }

        # If it's a reply to another comment, set the parent_comment_id from the request body
        parent_comment_id = data.get('parent_comment')
        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
            except Comment.DoesNotExist:
                return Response({"parent_comment": ["Invalid parent comment ID."]}, status=status.HTTP_400_BAD_REQUEST)

            comment_data['parent_comment'] = parent_comment_id

        serializer = CommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
