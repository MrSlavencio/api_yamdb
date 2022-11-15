from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewsViewSet,
                    UsersViewSet,
                    CommentsViewSet,
                    get_token,
                    sing_up,)


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

auth = [
    path('token/', get_token, name='get_token'),
    path('signup/', sing_up, name='signup')
]

urlpatterns = [
    path('auth/', include(auth)),
    path('', include(v1_router.urls)),
]
