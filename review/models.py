from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'food_item')  # one review per user per item
        ordering = ['-created_at']

    def __str__(self):
        food_title = self.food_item.title if self.food_item else "Deleted Item"
        return f"{self.user.username} - {food_title} ({self.rating}★)"


    @property
    def stars(self):
        return '⭐' * self.rating

