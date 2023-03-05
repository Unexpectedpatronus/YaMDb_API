from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet,
                    signup, token, ReviewViewSet, CommentViewSet)

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet, basename='users')
v1.register('genres', GenreViewSet, basename='genres')
v1.register('categories', CategoryViewSet, basename='categories')
v1.register('titles', TitleViewSet, basename='titles')
# v1.register(r'posts/(?P<post_id>\d+)/comments',
#                 ReviewViewSet, basename='reviews')
# v1.register(r'posts/(?P<post_id>\d+)/comments',
#                 CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='login'),
]
