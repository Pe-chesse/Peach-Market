from rest_framework import serializers
from .models import PostImage

class PostImageURLSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = PostImage
        fields = ['image_url']

    def get_image_url(self,obj):
        return obj.image.name
    
class ImageURLSerializer(serializers.Serializer):
    image_url = serializers.CharField() 