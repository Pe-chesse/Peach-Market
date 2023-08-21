# 데이터 처리
from .models import User, Product, Post, Comment
from .serializers import ProductSerializer, PostSerializer, CommentSerializer
# APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# user
from rest_framework.permissions import IsAuthenticated
from user.firebase import FirebaseAuthentication


# < Product >
# 상품 목록 조회
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# 상품 등록
class ProductWrite(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        serializer = ProductSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 상품 수정
class ProductUpdate(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        serializer = ProductSerializer(product, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 상품 삭제
class ProductDelete(APIView):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'msg': '상품 삭제가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


# 상품 상세 조회
class ProductDetail(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


# < Post >
# 게시글 목록 조회
class PostList(APIView):
    # Post list
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# 게시글 작성
class PostWrite(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 수정
class PostUpdate(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        request_data = request.data.copy()
        request_data['user'] = request.user.pk
        serializer = PostSerializer(post, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 게시글 삭제
class PostDelete(APIView):
    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({'msg':'게시글이 삭제되었습니다.'},status=status.HTTP_204_NO_CONTENT)


# 게시글 상세 조회
class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    # Post의 detail 보기
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


# < Comment >