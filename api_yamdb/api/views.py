from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleReadSerializer, TitleWriteSerializer, ReviewsSerializer
from django_filters.rest_framework import DjangoFilterBackend



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializerclass=ReviewsSerializer

    def get_queryset(self):
       title_id=self.kwargs.get('title_id') 
       title=get_object_or_404(Title, pk=title_id)
       return title.reviews.all()

    def perform_create(self, serializer):
        title_id=self.kwargs.get('title_id')
        title=get_object_or_404(Title, pk=title_id) 
        serializer.save(author=self.request.user, title_id=title)
