from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'cooking_time', 'price', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'ingredients', 'user__username')
    filter_horizontal = ('tags', 'ingredient_items')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
