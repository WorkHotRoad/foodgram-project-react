from django.db import models
from django.core.validators import RegexValidator


CHOICES = (
    ('#000000', 'черный'),
    ('#808080', 'серый'),
    ('#0000FF', 'синий'),
    ('#FF0000', 'красный'),
    ('#008000', 'зеленый'),
    ('#FFFF00', 'желтый'),
    ('#A52A2A', 'коричневый'),
    ('#FFFFFF', 'белый'),
    )


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True, choices=CHOICES)
    slug = models.CharField(
        max_length=200, 
        unique=True,
        validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$',)]
    )
