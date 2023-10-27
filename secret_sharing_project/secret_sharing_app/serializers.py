from rest_framework import serializers
from .models import Secret, SharedSecret
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')  # Include the fields you want to expose


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'private_key', 'public_key')  # Include the fields you want to expose


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = '__all__'


class SharedSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedSecret
        fields = '__all__'
