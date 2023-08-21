from .models import Post, User
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Q

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
class PostWrite(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404        
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data) 
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostSearchAPIView(APIView):
    def post(self, request, format=None):
        search_query = request.data.get("search_query")
        
        queryset = Post.objects.all()
        
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query)
            )
        
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
