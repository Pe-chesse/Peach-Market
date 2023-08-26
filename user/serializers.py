from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    followings_length = serializers.SerializerMethodField()
    followers_length = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email','nickname','image_url','description','followings_length','followers_length')

    def get_followers_length(self,obj):
        return obj.followers.count()
    
    def get_followings_length(self,obj):
        return obj.followings.count()
    
    def get_image_url(self,obj):
        try:
            return obj.image_url.profile_image.name
        except:
            return None

    
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','nickname', 'image_url']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname','followings')
