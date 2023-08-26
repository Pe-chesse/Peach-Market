import boto3
from django.db import models
from django.conf import settings
from post.models import Post,Product,User
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.files.storage import default_storage
from botocore.exceptions import NoCredentialsError

s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

class UserProfileImage(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='image_url')
    profile_image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.profile_image:
            uploaded_path = self.upload_to_s3(self.profile_image)
            self.profile_image = uploaded_path
        super(UserProfileImage, self).save(*args, **kwargs)

    def upload_to_s3(self, image):

        try:
            s3.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, image.name,ExtraArgs={"ACL": "public-read"})
            return f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image.name}'
        except NoCredentialsError:
            raise Exception('No AWS credentials provided')
    
    def __str__(self):
        return self.profile_image.name

@receiver(pre_delete, sender=UserProfileImage)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=instance.profile_image.name.split('/')[-1])

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True,blank=True,related_name='image_url')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True,related_name='image_url')
    image = models.ImageField(upload_to='posts/')
    
@receiver(pre_delete, sender=PostImage)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        default_storage.delete(instance.profile_image.name)