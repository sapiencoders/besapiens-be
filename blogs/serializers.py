from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from blogs.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all())

    class Meta:
        model = Post
        exclude = ['file']  # Exclude the file field


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


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
