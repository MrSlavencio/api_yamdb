from django.urls import path, include

from .views import GetTokenView, RegistrationView, UsersViewSet
from rest_framework.routers import SimpleRouter


v1_router = SimpleRouter()
v1_router.register('users', UsersViewSet, basename='users')

# urlpatterns = [
#     path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
#     path('v1/auth/signup/', RegistrationView.as_view(), name='registration'),
# ]

urlpatterns = [
    path('token/', GetTokenView.as_view(), name='get_token'),
    path('reg/', RegistrationView.as_view(), name='registration'),
    path('', include(v1_router.urls))
]
