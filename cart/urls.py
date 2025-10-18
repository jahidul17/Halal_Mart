from django.urls import path
from .views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
]
