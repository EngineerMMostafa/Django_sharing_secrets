from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_user, UserList, SecretViewSet, SharedSecretViewSet

router = DefaultRouter()
router.register(r'secrets', SecretViewSet)
router.register(r'shared-secrets', SharedSecretViewSet)

urlpatterns = [
    # path('user/register', include(router.urls)),
    path('user/register', register_user, name='register_user'),
    path('users', UserList.as_view(), name='user-list'),
]
