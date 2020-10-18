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
)

urlpatterns = [
    path("news/", PostListView.as_view()),
    path("news/<int:pk>/", PostDetailView.as_view()),
    path("news/<int:pk>/create_comment/", CommentCreateView.as_view(), name='olalala'),
    path("news/<int:pk>/create_rating/", RatingCreateView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

]
