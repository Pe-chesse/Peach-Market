import json
from django.core.cache import cache
from post.models import Post,Product
from user.models import User
from bucket.models import UserProfileImage,PostImage


def upload_redis_to_bucket(instance,image_key:str|list):

    match instance:
        case User():
            profile_image = cache.get(image_key)
            
            try:
                user_profile = UserProfileImage.objects.get(user=instance)
                user_profile.delete()
            
            except UserProfileImage.DoesNotExist:
                pass
            
            UserProfileImage.objects.create(user=instance, profile_image=profile_image)
            
        case Post():
            if type(image_key) == type(str()):
                image_key = json.loads(image_key)
            for i in image_key:
                post_image = cache.get(i)
                
                PostImage.objects.create(
                    post=instance, 
                    image=post_image)

        case Product():
            if type(image_key) == type(str()):
                image_key = json.loads(image_key)
            for i in image_key:
                post_image = cache.get(i)
                
                PostImage.objects.create(
                    product=instance, 
                    image=post_image)
        case _:
            print(type(instance))