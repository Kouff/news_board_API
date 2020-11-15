from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Post, Comment, Rating, User


class CustomModelSerializer(serializers.ModelSerializer):
    """ModelSerializer class with updated create method to add author to model creation"""

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)


class FilterCommentListSerializer(serializers.ListSerializer):
    """Filter for comments with parent = None"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Outputting recursively children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentListSerializer(CustomModelSerializer):
    """Comments output"""
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    children = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = '__all__'
        extra_kwargs = {'parent': {'write_only': True}, 'post': {'write_only': True}}


class RatingCreateSerializer(CustomModelSerializer):
    """Create rating"""

    class Meta:
        model = Rating
        exclude = ('id', 'author')
        extra_kwargs = {'post': {'write_only': True}}


class PostListSerializer(CustomModelSerializer):
    """Posts (news) output"""
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('author',)


class PostDetailSerializer(serializers.ModelSerializer):
    """Post (news) output in detail"""
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    rating = serializers.IntegerField(read_only=True)
    comments = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
