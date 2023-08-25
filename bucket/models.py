from django.db import models
from user.models import User
from post.models import Post
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage

class UserProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='image')
    profile_image = models.ImageField(upload_to='profiles/')

@receiver(pre_delete, sender=UserProfileImage)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        default_storage.delete(instance.profile_image.name)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='posts/')
    
@receiver(pre_delete, sender=PostImage)
def delete_user_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        default_storage.delete(instance.profile_image.name)

# class ChatImage(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE,related_name='images')
#     image = models.ImageField(upload_to='chats/')
#     expiration_date = models.DateTimeField()

#     def save(self, *args, **kwargs):
#         if not self.expiration_date:
#             self.expiration_date = timezone.now() + timezone.timedelta(days=30)
#         super(ChatImage, self).save(*args, **kwargs)