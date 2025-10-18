from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem 


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    city = models.CharField(max_length=100, default='Dhaka') 

    DELIVERY_FEES = {
        'dhaka': 70,
        'barisal': 80,
        'khulna': 100,
        'chittagong': 120,
    }

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def delivery_cost(self):
        return self.DELIVERY_FEES.get(self.city.lower(), 130)

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_price(self):
        return self.subtotal + self.delivery_cost


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'food_item')

    def __str__(self):
        return f"{self.food_item.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.food_item.price * self.quantity
