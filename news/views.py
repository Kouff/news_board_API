from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import models
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Post, Comment, Rating, User
from .permissions import IsAuthorOrReadOnly, IsMe
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentListSerializer,
    RatingCreateSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
)


class CustomCreateAPIView(CreateAPIView):
    """CreateAPIView class with updated create method to add post (news) id to serializer"""

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['post'] = self.kwargs['pk']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def get_posts():
    """Get all posts (news) with the field rating"""
    return Post.objects.all().annotate(rating=models.Count("rating_votes"))


class PostListView(ListCreateAPIView):
    """Display or create news"""
    queryset = get_posts()
    serializer_class = PostListSerializer


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """Display, edit or delete news"""
    queryset = get_posts()
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class CommentCreateView(CustomCreateAPIView):
    """Create comments"""
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer


class RatingCreateView(CustomCreateAPIView):
    """Creat rating"""
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    def create(self, request, *args, **kwargs):
        if Rating.objects.filter(author=request.user, post_id=self.kwargs['pk']).exists():
            # check for the existence of an object and display a message if the object already exists
            return Response({'vote': 'already been cast'}, status=status.HTTP_409_CONFLICT)
        else:
            response = super().create(request, *args, **kwargs)
            response.data['vote'] = 'accepted'
            return response


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsMe,)
