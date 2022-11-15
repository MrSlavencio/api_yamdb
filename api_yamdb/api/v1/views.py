from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator as tok_gen
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from .mixins import ModelMixinSet
from .filters import TitleFilter
from reviews.models import Category, Genre, Title, Review
from users.models import User
from users.permissions import (
    IsAdminUserOrReadOnly, AdminModeratorAuthorPermission, IsAdminOnly
)

from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer,
                          ReviewsSerializer,
                          ConfirmationCodeSerializer,
                          UserSerializer,
                          RegisrationSerializer,
                          CommentsSerializer)


def send_email(data):
    """Функция для отправки email с кодом подтверждения.
    На вход принимает словарь с темой письма, письмом и адресом.
    """
    email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        to=[data['to']]
    )
    email.send()


@api_view(['POST'])
@permission_classes((AllowAny,))
def sing_up(request):
    """
    Регистрация нового пользователя. Доступ для всех.
    Отправляется POST запрос с параметрами email и username.
    username 'me' запрещен.
    На указанный email отправляется код подтверждения.
    """

    serializer = RegisrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    confirmation_code = tok_gen.make_token(user)
    user.confirmation_code = confirmation_code
    email_body = (
        'Код подтверждения для получения токена для доступа на YaMDb:\n'
        f'{user.confirmation_code}'
    )
    data = {
        'subject': 'Код подтверждения для YaMDb',
        'body': email_body,
        'to': user.email,
    }
    send_email(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    """
    Получение или обновление токена для зарегистрированного пользователя.
    Отправляется POST запрос с параметрами username и confirmation_code,
    который был направлен на указанный email.
    Если пользователь существует и код верен, то в ответе будет токен.
    """
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        return Response(
            {'username': 'Пользователь не найден!'},
            status=status.HTTP_404_NOT_FOUND)
    if tok_gen.check_token(user, data.get('confirmation_code')):
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=status.HTTP_201_CREATED)
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Просмотр и изменение данных пользователя.
    Полный доступ для администратора.
    Пользователи имеют доступ только к своим данным.
    Доступ на смену роли пользователя есть только у админа.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @ action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        data = request.data
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            if not request.user.is_admin:
                serializer.validated_data["role"] = request.user.role
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class CategoryViewSet(ModelMixinSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
