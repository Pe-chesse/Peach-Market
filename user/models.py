from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, firebase_uid, username):
        user = self.model(
            firebase_uid=firebase_uid,
            username = username,
        )
        user.save(using=self._db)
        return user


class User(AbstractUser):
    firebase_uid = models.CharField(max_length=128,unique=True, db_index=True)
    email = models.EmailField()
    image_url = models.URLField(null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.email
    

class Follow(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f'{self.following_user} follow -> {self.followed_user}'