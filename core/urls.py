from django.urls import path

from .views import (
    PostListCreateAPIView,
    ListUserAPIView,
    CreateUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('users/', ListUserAPIView.as_view(), name='user-list'),
    path('users/create', CreateUserAPIView.as_view(), name='create-user'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view()),
]
