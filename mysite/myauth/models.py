from django.contrib.auth.models import User
from django.db import models


def user_avatar_path(instance: 'Profile', filename: str) -> str:
    return 'avatars/user_{pk}/{filename}'.format(
        pk=instance.username.pk,
        filename=filename,
    )


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_avatar_path)
