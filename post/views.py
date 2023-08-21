# 데이터 처리
from .models import Product, Post, Comment,Like
from .serializers import ProductSerializer, PostSerializer, PostListSerializer, CommentCreateSerializer,PostViewSerializer,LikeSerializer
# APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Q
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
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True,context={'request': request})
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


# 게시글 수정/삭제/댓글 작성
class PostAPIView(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if post.user != request.user:
                return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

            request_data = request.data.copy()
            request_data['user'] = request.user.pk
            serializer = PostSerializer(post, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("게시글을 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            
            if post.user != request.user:
                return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
            
            post.delete()
            return Response({'msg':'게시글이 삭제되었습니다.'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("게시글을 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, pk):
        try:
            comment_data = request.data.copy()
            comment_data['user'] = request.user.pk
            comment_data['post'] = pk
            serializer = CommentCreateSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BA_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class LikeAPIView(APIView):
    
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request,pk):
        like_data = {
            'user' : request.user.pk,
            'post' : pk
        }
        try:
            like = Like.objects.filter(user = request.user.pk,post = pk)
            if len(like) == 0:
                raise
            for i in like:
                i.delete()
            return Response('좋아요 취소',status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            try:
                like = LikeSerializer(data=like_data)
                if like.is_valid():
                    like.save()
                    return Response('좋아요',status=status.HTTP_200_OK)
                return Response(like.errors, status=400)
            except Exception as e:
                return Response(e,status=status.HTTP_404_NOT_FOUND)


# 게시글 상세 조회
class PostDetail(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk = pk)
            print(post)
            serialized_posts = PostViewSerializer(post,context={'request': request})
            # serialized_posts = PostViewSerializer(post)
            return Response(serialized_posts.data)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    def post(self, request, pk):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=pk)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BA_REQUEST)


# 댓글 수정, 삭제
class CommentDetailView(APIView):

    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            parent_comment = Comment.objects.get(pk = comment_id)
            comment_data = request.data.copy()
            comment_data['user'] = request.user.pk
            comment_data['post'] = parent_comment.post.pk
            comment_data['parent_comment'] = comment_id
            serializer = CommentCreateSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BA_REQUEST)
        except:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk = comment_id)
            if request.user != comment.user:
                return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

            comment_data = request.data.copy()
            comment_data['user'] = request.user.pk
            comment_data['post'] = comment.post.pk
            serializer = CommentCreateSerializer(comment, data=comment_data)
            if serializer.is_valid():
                serializer.save() # post에 user 정보 있기 때문에 (user=request.user) 생략
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response("댓글을 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)        


    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk = comment_id)
            if request.user != comment.user:
                return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
            
            comment.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)

        except:
            return Response("댓글을 찾을 수 없습니다.", status=status.HTTP_404_NOT_FOUND)


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
