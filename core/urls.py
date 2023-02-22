from django.urls import path

from .views import (
    PostListCreateAPIView,
    UserListAPIView,
    UserCreateAPIView,
    ProfileListAPIView,
    ProfileCreateAPIView,
    ProfileRetrieveUpdateDestroyAPIView,
    UserRetrieveUpdateDestroyAPIView,
)
from rest_framework.authtoken import views

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),

    path('profiles/', ProfileListAPIView.as_view(), name='profiles'),
    path('profiles/create/', ProfileCreateAPIView.as_view(), name='create-profile'),
    path('profiles/<int:pk>/', ProfileRetrieveUpdateDestroyAPIView.as_view()),

    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/create/', UserCreateAPIView.as_view(), name='create-user'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    path('auth-token/', views.obtain_auth_token, name='auth-token'),
]
