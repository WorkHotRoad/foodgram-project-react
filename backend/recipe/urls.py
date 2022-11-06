from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipe.views import IngredientsViewSet, RecipeViewSet, TagViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
