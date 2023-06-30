from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAuthorOrReadOnly, IsRoleAdmin, IsRoleModerator,
                          ReadOnly)
from .serializers import (AuthentificationSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitlePostSerializer,
                          TokenSerializer, UserSerializer)


class CreateListDestroy(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    permission_classes = (IsRoleAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = AuthentificationSerializer(
        data=request.data
    )
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        from_email=None,
        message=f'Ваш код подтверждения: {confirmation_code}',
        recipient_list=[user.email],
        subject='Код подтверждения'
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get('username')
    )

    if default_token_generator.check_token(user, serializer.validated_data.get(
            'confirmation_code')):
        refresh = RefreshToken.for_user(user)
        data = {'token': str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsRoleAdmin | ReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsRoleAdmin | ReadOnly,)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score')).order_by('-id')
    )
    permission_classes = (IsRoleAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleListSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsRoleAdmin | IsRoleModerator | IsAuthorOrReadOnly,
    )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
