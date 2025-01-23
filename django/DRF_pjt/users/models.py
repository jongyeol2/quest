from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to="images/", blank=True, default="images/기본프로필.jpg")
    bio = models.TextField(max_length=150, blank=True, default="")
