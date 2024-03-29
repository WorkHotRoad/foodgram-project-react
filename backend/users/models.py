from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                message="Имя может собержать только буквы,"
                "цыфры и знаки:'.', '@', '+', '-'"
            ), validate_username
        ]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["username"]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name="follower",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Имя подписчика"
    )
    following = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Имя автора"
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_entry'
            ),
        )
