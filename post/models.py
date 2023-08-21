from django.db import models
from user.models import User


# Create your models here.s
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    img_url = models.ImageField(null=True, upload_to="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    img_url = models.ImageField(null=True, upload_to="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body