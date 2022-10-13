from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_username
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, 
        validators=[
            RegexValidator(r'^[\w.@+-]+\Z',
            message="Password should be a combination of Alphabets and Numbers"
            ),validate_username
        ]
    )
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]
