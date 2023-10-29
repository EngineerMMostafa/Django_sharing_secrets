import base64

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import UserProfile, Secret, SharedSecret
from django.contrib.auth.models import User

from secret_sharing_app.serializers import UserProfileSerializer
from .encryption import generate_rsa_key_pair, generate_symmetric_key, \
    encrypt_secret, decrypt_secret, encrypt_symmetric_key, decrypt_symmetric_key
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
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

    shared_with_users = request.data.get('shared_with', [])
    for username in shared_with_users:
        try:
            user = User.objects.get(username=username)

            # skip secret owner
            if user == owner:
                continue

            recipient_profile = UserProfile.objects.get(user=user)

            # Encrypt the symmetric key with the recipient's public key
            encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, recipient_profile.public_key)

            shared_secret = SharedSecret(secret=secret, shared_with=user,
                                         encrypted_key_by_other_pbk=encrypted_symmetric_key)
            shared_secret.save()
        except ObjectDoesNotExist:
            print(f'usr {username} not found')

    return Response({'message': 'Secret created successfully'}, status=status.HTTP_201_CREATED)


def validate_request_private_key(data):
    private_key = data.get('private_key')
    if not private_key:
        raise Exception("Private_key is missing. This field is required.")

    try:
        parsed_private_key = base64.b64decode(data.get('private_key').encode('utf-8'))
        if not parsed_private_key.startswith(b'-----BEGIN PRIVATE KEY-----\n') or \
                not parsed_private_key.endswith(b'\n-----END PRIVATE KEY-----\n'):
            raise Exception
        return parsed_private_key
    except Exception:
        raise Exception("Invalid private_key.")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_secrets(request):
    try:
        private_key = validate_request_private_key(request.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    secrets = Secret.objects.filter(owner=request.user)

    decrypted_secrets = []
    for secret in secrets:
        decrypted_symmetric_key = decrypt_symmetric_key(secret.encrypted_key_by_owner_pbk, private_key)
        decrypted_content = decrypt_secret(secret.encrypted_content, decrypted_symmetric_key)
        decrypted_secret = {
            'content': decrypted_content,
            'created_at': secret.created_at,
        }
        decrypted_secrets.append(decrypted_secret)

    return Response({'secrets': decrypted_secrets})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_shared_secrets(request):
    try:
        private_key = validate_request_private_key(request.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    shared_secrets = SharedSecret.objects.filter(shared_with=request.user)

    decrypted_shared_secrets = []
    for shared_secret in shared_secrets:
        decrypted_symmetric_key = decrypt_symmetric_key(shared_secret.encrypted_key_by_other_pbk, private_key)
        decrypted_content = decrypt_secret(shared_secret.secret.encrypted_content, decrypted_symmetric_key)
        decrypted_secret = {
            'secret_owner': shared_secret.secret.owner.username,
            'content': decrypted_content,
            'created_at': shared_secret.secret.created_at,
        }
        decrypted_shared_secrets.append(decrypted_secret)

    return Response({'shared_secrets': decrypted_shared_secrets})
