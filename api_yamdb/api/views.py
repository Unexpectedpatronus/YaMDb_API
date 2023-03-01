from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from reviews.models import User
from .serializers import SignupSerializer, TokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK
    )


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения YaMDb'
    message = f'{confirmation_code} - ваш код для авторизации на YaMDb'
    admin_email = settings.ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
