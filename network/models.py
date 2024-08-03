from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_post")
    content = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_follow")

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, related_name="thread")
