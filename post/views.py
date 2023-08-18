# post/views.py
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from user.models import User

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'user__username']

    @action(detail=True, methods=['get'])
    def user_posts(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
