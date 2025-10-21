from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from cart.models import Cart, CartItem

class CheckoutView(APIView):
    def post(self, request):
        customer_name = request.data.get('customer_name')
        contact_number = request.data.get('contact_number')
        delivery_address = request.data.get('delivery_address')
        payment_method = request.data.get('payment_method')

        if not all([customer_name, contact_number, delivery_address, payment_method]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Determine cart
            if request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, _ = Cart.objects.get_or_create(session_key=session_key)

            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

            subtotal = sum(item.total_price for item in cart_items)
            delivery_cost = cart.delivery_cost
            total_amount = subtotal + delivery_cost

            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=customer_name,
                contact_number=contact_number,
                delivery_address=delivery_address,
                payment_method=payment_method,
                total_amount=total_amount
            )

            # Add items to order
            for item in cart_items:
                order.items.create(
                    food_item=item.food_item,
                    quantity=item.quantity,
                    price=item.food_item.price
                )

            # Clear user's or anonymous cart items
            cart_items.delete()

            return Response({
                'message': 'Order placed successfully.',
                'order_id': order.id,
                'total_amount': total_amount
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
