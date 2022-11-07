from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewsViewSet


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
#v1_router.register(r'reviews/(?P<titles_id>\d+)/reviews)', ReviewsViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]