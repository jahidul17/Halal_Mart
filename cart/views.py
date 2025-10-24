from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem
from menu.models import FoodItem

class CartView(APIView):
    DELIVERY_FEES = {
        'dhaka': 70,
        'barisal': 80,
        'khulna': 100,
        'chittagong': 120,
    }

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            return cart
        else:
            if 'cart' not in request.session:
                request.session['cart'] = {}
            if 'city' not in request.session:
                request.session['city'] = 'Dhaka'
            return request.session['cart']

    def save_cart_session(self, request, cart_data):
        request.session['cart'] = cart_data
        request.session.modified = True


    def get(self, request):
        if request.user.is_authenticated:
            cart = self.get_cart(request)
            data = {
                "city": cart.city,
                "subtotal": cart.subtotal,
                "delivery_cost": cart.delivery_cost,
                "total_price": cart.total_price,
                "items": [
                    {
                        "item_id": item.id,
                        "food_item_id": item.food_item.id,
                        "title": item.food_item.title,
                        "price": item.food_item.price,
                        "quantity": item.quantity,
                        "total_price": item.total_price
                    }
                    for item in cart.items.all()
                ]
            }
            return Response(data)
        else:
            cart = self.get_cart(request)
            city = request.session.get('city', 'Dhaka')
            delivery_cost = self.DELIVERY_FEES.get(city.lower(), 130)
            subtotal = sum(item['price']*item['quantity'] for item in cart.values())
            total_price = subtotal + delivery_cost
            items = [
                {
                    "food_item_id": key,
                    "title": value['title'],
                    "price": value['price'],
                    "quantity": value['quantity'],
                    "total_price": value['price']*value['quantity']
                } for key, value in cart.items()
            ]
            return Response({
                "city": city,
                "subtotal": subtotal,
                "delivery_cost": delivery_cost,
                "total_price": total_price,
                "items": items
            })


    def post(self, request):
        raw_food_id = request.data.get('food_item_id')
        if raw_food_id is None:
            return Response({'error': 'food_item_id is required'}, status=400)
        
        try:
            food_id = int(raw_food_id)
        except (ValueError, TypeError):
            return Response({'error': 'Invalid food_item_id'}, status=400)

        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            return Response({'error': 'Invalid quantity'}, status=400)

        try:
            food = FoodItem.objects.get(id=food_id)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=404)

        # Authenticated users
        if request.user.is_authenticated:
            cart = self.get_cart(request)
            item, created = CartItem.objects.get_or_create(cart=cart, food_item=food)
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()
            return Response({'message': 'Item added to cart (user)'})
        
        # Anonymous users
        cart = self.get_cart(request)  # this is session dict
        str_id = str(food_id)
        if str_id in cart:
            cart[str_id]['quantity'] += quantity
        else:
            cart[str_id] = {
                'title': food.title,
                'price': float(food.price),
                'quantity': quantity
            }
        self.save_cart_session(request, cart)
        return Response({'message': 'Item added to cart (anonymous)', 'cart': cart})


    def patch(self, request):
        city = request.data.get('city')
        raw_food_id = request.data.get('food_item_id')
        raw_quantity = request.data.get('quantity')

        if request.user.is_authenticated:
            cart = self.get_cart(request)
            if city:
                cart.city = city
                cart.save()
                return Response({'message': f'City updated to {city}'})
            if raw_food_id is not None and raw_quantity is not None:
                try:
                    food_id = int(raw_food_id)
                except (ValueError, TypeError):
                    return Response({'error': 'Invalid food_item_id'}, status=400)
                try:
                    quantity = int(raw_quantity)
                except (ValueError, TypeError):
                    return Response({'error': 'Invalid quantity'}, status=400)
                try:
                    item = CartItem.objects.get(cart=cart, food_item_id=food_id)
                    item.quantity = quantity
                    item.save()
                    return Response({'message': 'Quantity updated (user)'})
                except CartItem.DoesNotExist:
                    return Response({'error': 'Item not in cart'}, status=404)
            return Response({'error': 'No data provided'}, status=400)


    def delete(self, request):
        food_id = str(request.data.get('food_item_id'))

        if request.user.is_authenticated:
            cart = self.get_cart(request)
            try:
                item = CartItem.objects.get(cart=cart, food_item_id=food_id)
                item.delete()
                return Response({'message': 'Item removed from cart (user)'})
            except CartItem.DoesNotExist:
                return Response({'error': 'Item not in cart'}, status=404)
        else:
            cart = self.get_cart(request)
            if food_id in cart:
                del cart[food_id]
                self.save_cart_session(request, cart)
                return Response({'message': 'Item removed from cart (anonymous)'})
            else:
                return Response({'error': 'Item not in cart'}, status=404)


