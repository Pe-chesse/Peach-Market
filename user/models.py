from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username):
        user = self.model(
            username = username,
        )
        user.save(using=self._db)
        return user


class User(AbstractUser):

    image_url = models.URLField(null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self):
        return self.email