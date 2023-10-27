from django.urls import path
from .views import register_user, user_secrets, UserList, create_secret, user_shared_secrets

urlpatterns = [
    path('user/register', register_user, name='register_user'),
    path('user/secrets', user_secrets, name='retrieve_user_secrets'),
    path('user/shared_secrets', user_shared_secrets, name='retrieve_user_shared_secrets'),
    path('users', UserList.as_view(), name='user-list'),
    path('secrets/create', create_secret, name='create_secret'),
]
