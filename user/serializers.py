from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'image_url','nickname','description','followings')

    
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','nickname', 'image_url']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname','followings')
