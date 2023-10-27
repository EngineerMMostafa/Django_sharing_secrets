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
from .encryption import generate_rsa_key_pair, generate_symmetric_key, encrypt_secret, decrypt_secret


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
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_secret(request):
    owner = request.user
    content = request.data.get('content')

    symmetric_key = generate_symmetric_key()
    encrypted_content = encrypt_secret(content, symmetric_key)

    secret = Secret(owner=owner, content=content, encrypted_content=encrypted_content)
    secret.save()

    return Response({'message': 'Secret created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def user_secrets(request):
    secrets = Secret.objects.filter(owner=request.user)
    serializer = SecretSerializer(secrets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_shared_secrets(request):
    secrets = SharedSecret.objects.filter(shared_with=request.user)
    serializer = SecretSerializer(secrets, many=True)
    return Response(serializer.data)


class SharedSecretViewSet(viewsets.ModelViewSet):
    queryset = SharedSecret.objects.all()
    serializer_class = SharedSecretSerializer
    permission_classes = [IsOwnerOrSharedWith]
