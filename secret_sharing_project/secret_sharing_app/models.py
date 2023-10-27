from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key = models.BinaryField()
    public_key = models.BinaryField()


class Secret(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    encrypted_content = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


class SharedSecret(models.Model):
    secret = models.ForeignKey(Secret, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='secrets_shared_with')
