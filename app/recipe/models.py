from django.db import models
from django.conf import settings


class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    ingredient_items = models.ManyToManyField(
        Ingredient,
        blank=True,
        related_name='recipes',
    )
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
