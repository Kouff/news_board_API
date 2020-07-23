from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models

from .models import Post, Rating
from .serializers import PostListSerializer, CommentCreateSerializer, PostDetailSerializer, \
    PostCreateSerializer, RatingCreateSerializer


def add_author(request):
    """Добавление автора к post методу"""
    data = request.data
    data['author'] = request.user.pk
    return data


class PostListView(APIView):
    """Вывод списка новостей"""

    def get(self, request):
        posts = Post.objects.all().annotate(rating=models.Count("rating_votes"))
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailView(APIView):
    """Вывод всех комментариев к новости"""

    def get(self, request, id):
        post = Post.objects.get(pk=id)
        post.rating = post.rating_votes.count()
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostCreateView(APIView):
    """Добавление новости"""

    def post(self, request):
        post = PostCreateSerializer(data=add_author(request))
        if post.is_valid():
            post.save()
            return Response(status=201)
        return Response(status=400)


class CommentCreateView(APIView):
    """Добавление комментария"""

    def post(self, request):
        comment = CommentCreateSerializer(data=add_author(request))
        if comment.is_valid():
            comment.save()
            return Response(status=201)
        return Response(status=400)


class RatingCreateView(APIView):
    """Добавление голоса рейтинга"""

    def post(self, request):
        if 'post' in request.data:
            if Rating.objects.filter(post=Post.objects.get(pk=request.data['post']), author=request.user).exists():
                return Response(status=400, data="Нельзя повторно голосовать")
        rating = RatingCreateSerializer(data=add_author(request))
        if rating.is_valid():
            rating.save()
            return Response(status=201)
        return Response(status=400)
