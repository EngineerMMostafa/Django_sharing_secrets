import base64

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics

from .models import Secret, SharedSecret
from .serializers import SecretSerializer

from django.contrib.auth.models import User
from .models import UserProfile

from secret_sharing_app.serializers import UserProfileSerializer
from .encryption import generate_rsa_key_pair, generate_symmetric_key, \
    encrypt_secret, decrypt_secret, encrypt_symmetric_key, decrypt_symmetric_key
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            private_key, public_key = generate_rsa_key_pair()
            user = User.objects.create_user(username=username, password=password)
            user_profile, created = UserProfile.objects.get_or_create(user=user, public_key=public_key)
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)
            response_data = serializer.data
            response_data['private_key'] = base64.b64encode(private_key).decode('utf-8')
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
    user_profile = get_object_or_404(UserProfile, user=owner)

    symmetric_key = generate_symmetric_key()
    encrypted_content = encrypt_secret(content, symmetric_key)
    encrypted_key_by_owner_pbk = encrypt_symmetric_key(symmetric_key, user_profile.public_key)

    secret = Secret(owner=owner, encrypted_content=encrypted_content,
                    encrypted_key_by_owner_pbk=encrypted_key_by_owner_pbk)
    secret.save()

    return Response({'message': 'Secret created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def user_secrets(request):
    secrets = Secret.objects.filter(owner=request.user)
    decrypted_secrets = []
    if secrets:
        private_key = base64.b64decode(request.data.get('private_key').encode('utf-8'))
        for secret in secrets:
            decrypted_key = decrypt_symmetric_key(secret.encrypted_key_by_owner_pbk, private_key)
            decrypted_content = decrypt_secret(secret.encrypted_content, decrypted_key)
            decrypted_secret = {
                'content': decrypted_content,
                'created_at': secret.created_at,
            }
            decrypted_secrets.append(decrypted_secret)

    return Response({'Result': decrypted_secrets})


@api_view(['GET'])
def user_shared_secrets(request):
    secrets = SharedSecret.objects.filter(shared_with=request.user)
    serializer = SecretSerializer(secrets, many=True)
    return Response(serializer.data)
