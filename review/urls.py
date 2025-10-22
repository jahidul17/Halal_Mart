from django.urls import path
from .views import ReviewListCreateView, FoodItemRatingView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    path('average/<int:food_item_id>/', FoodItemRatingView.as_view(), name='food-average-rating'),
]


