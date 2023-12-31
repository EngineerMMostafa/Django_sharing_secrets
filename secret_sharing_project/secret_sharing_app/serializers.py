from rest_framework import serializers
from .models import Secret, SharedSecret
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'username')


class SecretSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Secret
        fields = '__all__'


class SharedSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedSecret
        fields = '__all__'
