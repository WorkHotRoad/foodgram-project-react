from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
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
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название тэга",
    )
    color = models.CharField(
        max_length=7, choices=CHOICES,
        unique=True,
        verbose_name="Цвет в HEX",
    )
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
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единица измерения"
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique ingredients"
            )
        ]
        ordering = ["name"]
        verbose_name ='Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Имя автора",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта"
    )
    text = models.TextField(
        verbose_name="Описание рецепта"
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'),
        ),
        verbose_name='Время приготовления в минутах'
    )
    image = models.ImageField(
        upload_to='images_recipe',
        verbose_name="Картинка рецепта"
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        through="IngredientAmount",
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )

    def __str__(self):
        return self.name

    class Meta:

         ordering = ['-id']
         verbose_name = 'Рецепт'
         verbose_name_plural = 'Рецепты'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            1, message='Минимальное количество 1'),
        ),
        verbose_name='Количество'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"], name="unique ingredients_recipe"
            )
        ]
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Favorite(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name="рецепт"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "recipe"], name="favorite_unique_recipe"
            )
        ]
        ordering = ['-id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    author = models.ForeignKey(
        User,
        related_name='Shopping_list',
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='Shopping_list',
        on_delete=models.CASCADE,
        verbose_name="Рецепт"
    )
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепты для покупки'
        verbose_name_plural = 'Рецепты для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipe'], name='unique shopping_list')
        ]











