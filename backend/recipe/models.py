from django.db import models
from django.core.validators import RegexValidator
from users.models import User


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
    name = models.CharField(max_length=200, verbose_name="Название тэга")
    color = models.CharField(max_length=7, choices=CHOICES, verbose_name="Цвет в HEX")
    slug = models.CharField(
        max_length=200,
        unique=True,
        validators=[RegexValidator(r'^[-a-zA-Z0-9_]+$',)],
        verbose_name="Уникальный слаг"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Ingredients(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ингредиента")
    measurement_unit = models.CharField(max_length=200, verbose_name="Мера измерений")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique ingredients"
            )
        ]
        ordering = ["name"]
        verbose_name ='Ингридиенты'


# class Measurement_system(models.Model):
#     num = models.PositiveSmallIntegerField()


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Имя автора Автор",
#     )
#     name = models.CharField(max_length=200, verbose_name="Название рецепта")
#     description = models.TextField(verbose_name="Описание")
#     cooking_time = models.TimeField(verbose_name="Время приготовления в минутах")
#     foto = models.URLField(verbose_name="Фотография")
#     ingredients = models.ManyToManyField(Ingredients, on_delete=models.CASCADE)
#     tag = models.ManyToManyField(Tag, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name










