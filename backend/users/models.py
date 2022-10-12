from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username

# validators=(validate_username,),

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]
