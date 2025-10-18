from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'Piece'),
        ('kg', 'Kilogram'),
        ('ltr', 'Liter'),
        ('gm', 'Gram'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='foods')
    title = models.CharField(max_length=200)
    sold_by = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
