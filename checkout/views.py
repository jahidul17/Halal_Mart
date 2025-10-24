from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from cart.models import Cart, CartItem
from cart.views import CartView 

class CheckoutView(APIView):
    """
    Checkout API for logged-in and anonymous users.
    Anonymous carts are stored in session.
    """
    def post(self, request):
        customer_name = request.data.get('customer_name')
        contact_number = request.data.get('contact_number')
        delivery_address = request.data.get('delivery_address')
        payment_method = request.data.get('payment_method', 'cash')

        if not all([customer_name, contact_number, delivery_address]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # ------------------ GET CART ------------------
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            subtotal = sum(item.total_price for item in cart_items)
            delivery_cost = cart.delivery_cost
        else:
            session_cart = request.session.get('cart', {})
            if not session_cart:
                return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            cart_items = session_cart  # dict
            subtotal = sum(info['price'] * info['quantity'] for info in session_cart.values())
            city = request.session.get('city', 'Dhaka')
            delivery_cost = CartView.DELIVERY_FEES.get(city.lower(), 130)

        total_amount = subtotal + delivery_cost

        # ------------------ CREATE ORDER ------------------
        try:
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=customer_name,
                contact_number=contact_number,
                delivery_address=delivery_address,
                payment_method=payment_method,
                total_amount=total_amount
            )

            # ------------------ ADD ITEMS ------------------
            if request.user.is_authenticated:
                for item in cart_items:
                    order.items.create(
                        food_item=item.food_item,
                        quantity=item.quantity,
                        price=item.food_item.price
                    )
                # Clear cart items
                cart_items.delete()
            else:
                for food_id, info in cart_items.items():
                    order.items.create(
                        food_item_id=int(food_id),
                        quantity=info['quantity'],
                        price=info['price']
                    )
                # Clear session cart
                request.session['cart'] = {}
                request.session.modified = True

            return Response({
                'message': 'Order placed successfully.',
                'order_id': order.id,
                'total_amount': total_amount
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

