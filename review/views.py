from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Review
from .serializers import ReviewSerializer
from menu.models import FoodItem
from django.db.models import Avg

class ReviewListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        rating_filter = request.query_params.get('rating')
        food_item_id = request.query_params.get('food_item')

        reviews = Review.objects.all()

        if food_item_id:
            reviews = reviews.filter(food_item_id=food_item_id)
        if rating_filter:
            reviews = reviews.filter(rating=rating_filter)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            food_item = serializer.validated_data['food_item']

            existing_review = Review.objects.filter(user=request.user, food_item=food_item).first()
            if existing_review:
                return Response(
                    {'error': 'You have already reviewed this food item.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class FoodItemRatingView(APIView):
    """Returns average rating of a specific food item"""
    def get(self, request, food_item_id):
        try:
            food_item = FoodItem.objects.get(id=food_item_id)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=404)

        avg_rating = food_item.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        return Response({
            'food_item': food_item.title,
            'average_rating': round(avg_rating, 1),
        })

