from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .mixins import ModelMixinSet
from .filters import TitleFilter
from reviews.models import Category, Genre, Title
from users.models import User
from users.permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer,
                          ReviewsSerializer,
                          GetTokenSerializer,
                          StuffUserSerializer,
                          UserSerializer,
                          RegisrationSerializer,)


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

    queryset = Title.objects.all()  # Добавить столбец со столбцом с средней оценкой
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializerclass = ReviewsSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title_id=title)


class RegistrationView(APIView):
    """
    Регистрация нового пользователя. Доступ для всех.
    Отправляется POST запрос с параметрами email и username.
    username 'me' запрещен.
    На указанный email отправляется код подтверждения.
    """

    permission_classes = (AllowAny,)

    @ staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to']]
        )
        email.send()

    def post(self, request):
        serializer = RegisrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            'Код подтверждения для получения токена для доступа на YaMDb:\n'
            f'{user.confirmation_code}'
        )
        data = {
            'subject': 'Код подтверждения для YaMDb',
            'body': email_body,
            'to': user.email,
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """
    Получение или обновление токена для зарегистрированного пользователя.
    Отправляется POST запрос с параметрами username и confirmation_code,
    который был направлен на указанный email.
    Если пользователь существует и код верен, то в ответе будет токен.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
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
    serializer_class = StuffUserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)
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
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = StuffUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
