from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=150)
    link = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    amount_of_upvotes = models.SmallIntegerField()
    author_name = models.CharField(max_length=50)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author_name = models.CharField(max_length=50)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
