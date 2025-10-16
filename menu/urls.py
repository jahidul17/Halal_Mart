from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FoodItemViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('foods', FoodItemViewSet, basename='food')

urlpatterns = router.urls
