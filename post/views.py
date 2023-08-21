# 데이터 처리
from .models import User, Product, Post, Comment
from .serializers import ProductSerializer, PostSerializer, CommentSerializer, CommentCreateSerializer
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
    def get(self, request, pk):
        post = Post.objects.prefetch_related('comment_set').get(pk=pk)
        
        comments = post.comment_set.all()
        serialized_comments = CommentSerializer(comments, many=True).data
        
        data = {
            'post_id': pk,
            'comments': serialized_comments,
        }
        return Response(data)
        


# < Comment >
# 댓글 리스트, 작성
class CommentView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 댓글 수정, 삭제
class CommentDetailView(APIView):
    def put(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save() # post에 user 정보 있기 때문에 (user=request.user) 생략
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else: 
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)