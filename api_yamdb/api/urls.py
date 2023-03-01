from django.urls import path

from .views import signup, token


urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='login'),
]