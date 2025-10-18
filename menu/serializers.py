from rest_framework import serializers
from .models import Category, FoodItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FoodItemSerializer(serializers.ModelSerializer):
    # category_name = serializers.ReadOnlyField(source='category.name') #it show only id
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FoodItem
        fields = '__all__'


