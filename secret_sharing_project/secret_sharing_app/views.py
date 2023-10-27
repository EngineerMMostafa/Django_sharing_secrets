from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, viewsets

from .models import Secret, SharedSecret
from .serializers import SecretSerializer, SharedSecretSerializer
from .permissions import IsOwnerOrSharedWith

from django.contrib.auth.models import User
from .models import UserProfile

from secret_sharing_app.serializers import UserProfileSerializer
from .encryption import generate_rsa_key_pair, encrypt_secret, decrypt_secret


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            private_key, public_key = generate_rsa_key_pair()
            user = User.objects.create_user(username=username, password=password)
            user_profile, created = UserProfile.objects.get_or_create(user=user, private_key=private_key, public_key=public_key)
            # user_profile.private_key = private_key
            # user_profile.public_key = public_key
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)  # Assuming you have a UserSerializer
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    permission_classes = [IsOwnerOrSharedWith]

    def perform_create(self, serializer):
        private_key, public_key = generate_rsa_key_pair()
        owner = self.request.user
        secret = serializer.save(owner=owner)
        secret.encrypted_secret = encrypt_secret(public_key, secret.content)
        secret.private_key = private_key
        secret.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == request.user:
            content = decrypt_secret(instance.private_key, instance.encrypted_secret)
            return Response({'content': content})
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)


class SharedSecretViewSet(viewsets.ModelViewSet):
    queryset = SharedSecret.objects.all()
    serializer_class = SharedSecretSerializer
    permission_classes = [IsOwnerOrSharedWith]
