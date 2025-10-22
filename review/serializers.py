from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    stars = serializers.CharField(source='stars', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'food_item', 'rating', 'stars', 'comment', 'created_at']



