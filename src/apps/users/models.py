from django.contrib.auth.models import AbstractUser
from django.db import models


class TrelloUser(AbstractUser):
    avatar = models.ImageField(null=True, verbose_name="Profile picture", blank=True)
