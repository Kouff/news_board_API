from django.urls import path

from .views import PostListView, PostDetailView, CommentCreateView, PostCreateView, RatingCreateView

urlpatterns = [
    path('news/', PostListView.as_view()),
    path('news/<int:id>/', PostDetailView.as_view()),
    path('create_comment/', CommentCreateView.as_view()),
    path('create_news/', PostCreateView.as_view()),
    path('create_rating/', RatingCreateView.as_view()),
]
