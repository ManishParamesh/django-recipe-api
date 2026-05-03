from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializer(many=True, read_only=True)
    ingredient_items = IngredientSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False,
    )
    ingredient_item_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient_items',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'user',
            'title',
            'description',
            'ingredients',
            'instructions',
            'cooking_time',
            'price',
            'image',
            'tags',
            'ingredient_items',
            'tag_ids',
            'ingredient_item_ids',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_tag_ids(self, value):
        return self._validate_owned_items(value, 'tag')

    def validate_ingredient_item_ids(self, value):
        return self._validate_owned_items(value, 'ingredient')

    def _validate_owned_items(self, value, label):
        request = self.context.get('request')
        if not request:
            return value

        invalid_items = [item.id for item in value if item.user_id != request.user.id]
        if invalid_items:
            raise serializers.ValidationError(
                f'Invalid {label} ids for this user: {invalid_items}'
            )

        return value
