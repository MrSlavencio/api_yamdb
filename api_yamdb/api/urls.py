from django.urls import include, path
from rest_framework import routers
from .views import CategoryViewSet


app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
