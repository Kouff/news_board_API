from rest_framework import serializers

from .models import Post, Comment, Rating


class PostListSerializer(serializers.ModelSerializer):
    """Список новостей"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Post
        fields = "__all__"


class FilterCommentListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, у которых parent=None"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Вывод комментариев"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        exclude = ("post", "parent")


class PostDetailSerializer(serializers.ModelSerializer):
    """Список новостей"""

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    rating = serializers.IntegerField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    """Добавление новости"""

    class Meta:
        model = Post
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    """Добавление комементариев"""

    class Meta:
        model = Comment
        fields = "__all__"


class RatingCreateSerializer(serializers.ModelSerializer):
    """Добавление голоса рейтинга"""

    class Meta:
        model = Rating
        fields = "__all__"
