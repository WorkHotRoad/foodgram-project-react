from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipe.views import TagViewSet, IngredientsViewSet, RecipeViewSet

app_name = 'recipe'

router = DefaultRouter()
router.register(r'tags', TagViewSet) 
router.register(r'ingredients', IngredientsViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]