from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise ValidationError(
                'Пользователь может оставлять только один '
                'отзыв на произведение'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class RegisrationSerializer(serializers.ModelSerializer):
    """Для регистрации нового пользователя."""

    username = serializers.CharField(
        required=True, max_length=150, validators=[UnicodeUsernameValidator])
    email = serializers.EmailField(
        required=True, max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Имя пользователя не может быть "me".'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким username уже существует.")
        return value

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует.")
        return lower_email

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    """Для получения и обновления токена пользователя."""
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Для просмотра и изменения данных пользователей админом.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
