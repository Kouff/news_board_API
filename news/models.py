from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=150)
    link = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    creation_date = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    post = models.ForeignKey(
        Post, related_name="rating_votes", on_delete=models.CASCADE
    )
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
