from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from cart.models import CartItem
from .serializers import OrderSerializer

class CheckoutView(APIView):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        data = request.data

        # Get all cart items for this user (adjust if you have session-based cart)
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.total_price for item in cart_items)

        order = Order.objects.create(
            user=user,
            customer_name=data.get('customer_name'),
            contact_number=data.get('contact_number'),
            delivery_address=data.get('delivery_address'),
            payment_method=data.get('payment_method'),
            total_amount=total,
        )

        # Copy items from cart to order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.food.name,   # or item.product_name if your model differs
                quantity=item.quantity,
                price=item.food.price,
            )

        # Clear cart
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
