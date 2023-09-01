from .models import Product, Post, Comment, Like
from user.models import User
from user.serializers import PublicUserSerializer
from bucket.serializers import PostImageURLSerializer
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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def get_comment_length(self, obj):
        return obj.comment_set.count()
    
    def get_like_length(self, obj):
        return obj.like_set.count()
    
    def get_is_like(self, obj):
        try:
            obj.like_set.get(user=self.request.user)
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_image_url(self, obj):
        return [i.image.name for i in obj.image_url.all()]
        
    
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostViewSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('context').get('request')
        super(PostViewSerializer, self).__init__(*args, **kwargs)
    user = PublicUserSerializer()
    comment_set = serializers.SerializerMethodField()
    like_length = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','body','user','image_url','updated_at','created_at','comment_set','like_length','is_like']

    def get_comment_set(self, obj):
        comment_set = obj.comment_set.filter(status = False,parent_comment = None)
        print(comment_set)
        serializer = CommentViewSerializer(comment_set, many=True,context={'request': self.request})
        return serializer.data
    
    def get_like_length(self, obj):
        return obj.like_set.count()
    
    def get_is_like(self, obj):
        try:
            obj.like_set.get(user=self.request.user)
            return True
        except Exception as e:
            print(e)
            return False
    
    def get_image_url(self, obj):
        return [i.image.name for i in obj.image_url.all()]
        

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
        child_comments = obj.child_comments.filter(status = False)
        serializer = CommentViewSerializer(child_comments, many=True,context={'request': self.request})
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'