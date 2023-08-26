from .models import Product, Post, Comment, Like
from user.models import User
from user.serializers import PublicUserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()
    class Meta:
        model = Product
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context').get('request')
        super(PostListSerializer, self).__init__(*args, **kwargs)

    user = PublicUserSerializer()
    comment_length = serializers.SerializerMethodField()
    like_length = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def get_comment_length(self, obj):
        return obj.comment_set.count()
    
    def get_like_length(self, obj):
        return obj.like_set.count()
    
    def get_is_like(self, obj):
        try:
            request_user = self.request.user
            return obj.like_set.filter(user=request_user).exists()
        except:
            return False
        
    
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostViewSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context').get('request')
        super(PostListSerializer, self).__init__(*args, **kwargs)
    user = PublicUserSerializer()
    comment_set = serializers.SerializerMethodField()
    like_set_length = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','body','user','img_url','updated_at','created_at','comment_set','like_set_length','is_like']

    def get_comment_set(self, obj):
        comment_set = obj.comment_set.filter(status = True,parent_comment = None)
        serializer = CommentViewSerializer(comment_set, many=True,context={'request': self.request})
        return serializer.data
    
    def get_like_set_length(self, obj):
        return obj.like_set.count()
    
    def get_is_like(self, obj):
        try:
            request_user = self.request.user
            return obj.like_set.filter(user=request_user).exists()
        except:
            return False


class CommentViewSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context').get('request')
        super(CommentViewSerializer, self).__init__(*args, **kwargs)
    user = PublicUserSerializer()
    child_comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','body','user','child_comments','updated_at','created_at']
        

    def get_child_comments(self, obj):
        child_comments = obj.child_comments.filter(status = True)
        serializer = CommentViewSerializer(child_comments, many=True,context={'request': self.request})
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'