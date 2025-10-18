from rest_framework import serializers
from .models import Cart, CartItem
from menu.serializers import FoodItemSerializer


class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset=CartItem.objects.none(),  # will override in view
        source='food_item',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'food_item_id', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.ReadOnlyField()
    delivery_cost = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'city', 'items', 'subtotal', 'delivery_cost', 'total_price']


