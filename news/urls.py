from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    PostListView,
    PostDetailView,
    CommentCreateView,
    RatingCreateView,
    UserCreateView,
    UserDetailView,
)

urlpatterns = [
    path("news/", PostListView.as_view()),
    path("news/<int:pk>/", PostDetailView.as_view()),
    path("news/<int:pk>/create_comment/", CommentCreateView.as_view()),
    path("news/<int:pk>/create_rating/", RatingCreateView.as_view()),
    path("user/", UserCreateView.as_view()),
    path("user/<int:pk>/", UserDetailView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]
