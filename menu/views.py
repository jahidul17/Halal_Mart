from rest_framework import viewsets, filters, permissions
from .models import Category, FoodItem
from .serializers import CategorySerializer, FoodItemSerializer
from django_filters.rest_framework import DjangoFilterBackend

# only admin can modify
class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]


class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all().order_by('-id')
    serializer_class = FoodItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'availability']
    search_fields = ['title', 'brand']
    permission_classes = [AdminOrReadOnly]

