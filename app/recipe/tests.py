from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ingredient, Recipe, Tag


class RecipeApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='cook',
            password='testpass123',
        )
        self.payload = {
            'title': 'Tomato Rice',
            'description': 'Simple weekday meal',
            'ingredients': 'Rice, tomato, onion, spices',
            'instructions': 'Cook rice. Saute vegetables. Mix and simmer.',
            'cooking_time': 30,
            'price': '20.00',
        }

    def test_authenticated_user_can_create_recipe(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(reverse('recipe-list'), self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get()
        self.assertEqual(recipe.title, self.payload['title'])
        self.assertEqual(recipe.user, self.user)

    def test_anonymous_user_cannot_create_recipe(self):
        response = self.client.post(reverse('recipe-list'), self.payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_anonymous_user_can_list_recipes(self):
        Recipe.objects.create(user=self.user, **self.payload)

        response = self.client.get(reverse('recipe-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_create_tag_and_ingredient(self):
        self.client.force_authenticate(self.user)

        tag_response = self.client.post(reverse('tag-list'), {'name': 'Dinner'})
        ingredient_response = self.client.post(
            reverse('ingredient-list'),
            {'name': 'Tomato'},
        )

        self.assertEqual(tag_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ingredient_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_user_can_attach_tag_and_ingredient_to_recipe(self):
        self.client.force_authenticate(self.user)
        tag = Tag.objects.create(user=self.user, name='Dinner')
        ingredient = Ingredient.objects.create(user=self.user, name='Tomato')
        payload = {
            **self.payload,
            'tag_ids': [tag.id],
            'ingredient_item_ids': [ingredient.id],
        }

        response = self.client.post(reverse('recipe-list'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get()
        self.assertEqual(list(recipe.tags.all()), [tag])
        self.assertEqual(list(recipe.ingredient_items.all()), [ingredient])
