from rest_framework import serializers

from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Posts model"""
    class Meta:
        model = Post
        fields = ['title', 'description', 'poster']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a post"""
        post = Post.objects.create(**validated_data, poster=self.context['request'].user)
        return post


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
