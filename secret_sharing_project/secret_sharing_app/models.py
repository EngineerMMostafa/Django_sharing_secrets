from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.BinaryField()


class Secret(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    encrypted_content = models.BinaryField()
    encrypted_key_by_owner_pbk = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)


class SharedSecret(models.Model):
    secret = models.ForeignKey(Secret, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    encrypted_key_by_other_pbk = models.BinaryField()
