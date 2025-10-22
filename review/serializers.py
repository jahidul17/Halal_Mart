from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    full_name=serializers.SerializerMethodField()
    food_item=serializers.CharField(source='food_item.title', read_only=True)
    stars = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user','full_name', 'food_item', 'rating', 'stars', 'comment', 'created_at']

    def get_full_name(self, obj):
        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        full_name = f"{first_name} {last_name}".strip()
        return full_name

    def get_stars(self, obj):
        return '⭐' * obj.rating

