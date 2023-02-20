from django.urls import path

from .views import (
    PostListCreateAPIView,
    ListUserAPIView,
    CreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
)
from rest_framework.authtoken import views

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('users/create', CreateUserAPIView.as_view(), name='create-user'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('auth-token/', views.obtain_auth_token, name='auth-token'),
]
