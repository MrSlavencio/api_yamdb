from rest_framework import viewsets
from reviews.models import Categories
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
