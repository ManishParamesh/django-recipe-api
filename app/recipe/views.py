from rest_framework import permissions, viewsets

from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Recipe.objects.select_related('user').prefetch_related(
            'tags',
            'ingredient_items',
        )
        tag_ids = self.request.query_params.get('tags')
        ingredient_ids = self.request.query_params.get('ingredients')

        if tag_ids:
            queryset = queryset.filter(tags__id__in=self._split_ids(tag_ids))

        if ingredient_ids:
            queryset = queryset.filter(
                ingredient_items__id__in=self._split_ids(ingredient_ids)
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _split_ids(self, value):
        return [item for item in value.split(',') if item.strip().isdigit()]


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(UserOwnedModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(UserOwnedModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
