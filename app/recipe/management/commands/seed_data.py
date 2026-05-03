from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipe.models import Ingredient, Recipe, Tag


class Command(BaseCommand):
    help = 'Create sample recipe API data.'

    def handle(self, *args, **options):
        user = self._create_user()
        tags = self._create_tags(user)
        ingredients = self._create_ingredients(user)
        created, updated = self._create_recipes(user, tags, ingredients)

        self.stdout.write(
            self.style.SUCCESS(
                f'Sample data ready: {created} recipes created, '
                f'{updated} recipes updated, {len(tags)} tags, '
                f'{len(ingredients)} ingredients. Login: chef / testpass123'
            )
        )

    def _create_user(self):
        user, _ = get_user_model().objects.get_or_create(
            username='chef',
            defaults={
                'email': 'chef@example.com',
                'first_name': 'Demo',
                'last_name': 'Chef',
            },
        )
        user.set_password('testpass123')
        user.save()
        return user

    def _create_tags(self, user):
        tag_names = ['Breakfast', 'Dinner', 'Vegetarian', 'Quick', 'Indian']
        return {
            name: Tag.objects.get_or_create(user=user, name=name)[0]
            for name in tag_names
        }

    def _create_ingredients(self, user):
        ingredient_names = [
            'Rice',
            'Tomato',
            'Onion',
            'Paneer',
            'Egg',
            'Milk',
            'Butter',
            'Garlic',
            'Potato',
            'Green chili',
        ]
        return {
            name: Ingredient.objects.get_or_create(user=user, name=name)[0]
            for name in ingredient_names
        }

    def _create_recipes(self, user, tags, ingredients):
        samples = [
            {
                'title': 'Tomato Rice',
                'description': 'A quick and spicy rice dish for lunch or dinner.',
                'ingredients': 'Rice, tomato, onion, garlic, green chili, spices',
                'instructions': (
                    'Cook rice. Saute onion, garlic, tomato, and chili. '
                    'Add spices, mix rice, and simmer for 5 minutes.'
                ),
                'cooking_time': 30,
                'price': '45.00',
                'tags': ['Dinner', 'Quick', 'Indian'],
                'ingredient_items': [
                    'Rice',
                    'Tomato',
                    'Onion',
                    'Garlic',
                    'Green chili',
                ],
            },
            {
                'title': 'Paneer Butter Masala',
                'description': 'Creamy paneer curry with a rich tomato-butter base.',
                'ingredients': 'Paneer, tomato, butter, milk, onion, garlic, spices',
                'instructions': (
                    'Cook onion, tomato, and garlic until soft. Blend into a sauce. '
                    'Add butter, milk, spices, and paneer. Simmer until creamy.'
                ),
                'cooking_time': 45,
                'price': '120.00',
                'tags': ['Dinner', 'Vegetarian', 'Indian'],
                'ingredient_items': [
                    'Paneer',
                    'Tomato',
                    'Butter',
                    'Milk',
                    'Onion',
                    'Garlic',
                ],
            },
            {
                'title': 'Masala Omelette',
                'description': 'Fast breakfast omelette with onion, tomato, and chili.',
                'ingredients': 'Egg, onion, tomato, green chili, butter',
                'instructions': (
                    'Beat eggs with chopped vegetables. Heat butter in a pan, '
                    'pour mixture, cook both sides, and serve hot.'
                ),
                'cooking_time': 12,
                'price': '35.00',
                'tags': ['Breakfast', 'Quick'],
                'ingredient_items': [
                    'Egg',
                    'Onion',
                    'Tomato',
                    'Green chili',
                    'Butter',
                ],
            },
            {
                'title': 'Aloo Fry',
                'description': 'Crispy potato side dish with simple spices.',
                'ingredients': 'Potato, onion, garlic, green chili, spices',
                'instructions': (
                    'Slice potatoes. Fry onion, garlic, and chili. Add potatoes '
                    'and spices, then cook until crisp.'
                ),
                'cooking_time': 25,
                'price': '40.00',
                'tags': ['Vegetarian', 'Quick', 'Indian'],
                'ingredient_items': ['Potato', 'Onion', 'Garlic', 'Green chili'],
            },
        ]

        created = 0
        updated = 0

        for item in samples:
            recipe, was_created = Recipe.objects.get_or_create(
                user=user,
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'ingredients': item['ingredients'],
                    'instructions': item['instructions'],
                    'cooking_time': item['cooking_time'],
                    'price': item['price'],
                },
            )

            if was_created:
                created += 1
            else:
                updated += 1
                recipe.description = item['description']
                recipe.ingredients = item['ingredients']
                recipe.instructions = item['instructions']
                recipe.cooking_time = item['cooking_time']
                recipe.price = item['price']
                recipe.save()

            recipe.tags.set(tags[name] for name in item['tags'])
            recipe.ingredient_items.set(
                ingredients[name] for name in item['ingredient_items']
            )

        return created, updated
