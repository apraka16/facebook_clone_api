from django.urls import path

from .views import (
    PostListCreateAPIView,
    PostRetrieveAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,

    UserListAPIView,
    UserCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserPostListAPIView,

    ProfileListAPIView,
    ProfileCreateAPIView,
    ProfileRetrieveUpdateDestroyAPIView,

)
from rest_framework.authtoken import views

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(),
         name='posts'),
    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(),
         name='post-details'),
    path('posts/update/<int:pk>', PostUpdateAPIView.as_view(),
         name='post-update'),
    path('posts/delete/<int:pk>', PostDeleteAPIView.as_view(),
         name='post-delete'),
    path('posts/poster/<int:poster_id>', UserPostListAPIView.as_view(),
         name='user-posts'),

    path('profiles/', ProfileListAPIView.as_view(),
         name='profiles'),
    path('profiles/create/', ProfileCreateAPIView.as_view(),
         name='create-profile'),
    path('profiles/<int:pk>/', ProfileRetrieveUpdateDestroyAPIView.as_view()),

    path('users/', UserListAPIView.as_view(),
         name='user-list'),
    path('users/create/', UserCreateAPIView.as_view(),
         name='create-user'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(),
         name='user-detail'),

    path('auth-token/', views.obtain_auth_token,
         name='auth-token'),
]
