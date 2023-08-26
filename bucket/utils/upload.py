import boto3
from botocore.exceptions import NoCredentialsError
from django.core.cache import cache
from django.conf import settings
from post.models import Post,Product
from user.models import User
from bucket.models import UserProfileImage,PostImage


def upload_redis_to_bucket(instance,image_key:str|list):

    s3 = boto3.client("s3")
    match instance:
        case User():
            profile_image = cache.get(image_key)
            try:
                user_profile = UserProfileImage.objects.get(user=instance)
                user_profile.delete()
            except UserProfileImage.DoesNotExist:
                pass
            
            user_profile = UserProfileImage.objects.create(user=instance, profile_image=profile_image)
            
        case Product():
            print(instance)
            print('Product')
        case Post():
            print(instance)
            print(type(instance))
            print('Post')
        case _:
            print('ㄴㄴ')