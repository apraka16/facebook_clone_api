from rest_framework import serializers

from .models import Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile model"""
    class Meta:
        model = UserProfile
        fields = ['dob', 'country', 'aboutme']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create the uesr's profile"""
        profile = UserProfile.objects.create(
            **validated_data,
            user=self.context['request'].user
        )
        return profile

    def update(self, instance, validated_data):
        """Update and return profile"""
        profile = super().update(instance, validated_data)
        return profile


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
        fields = ['poster', 'title', 'description']
        depth = 1
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a post"""
        post = Post.objects.create(**validated_data, poster=self.context['request'].user)
        return post
