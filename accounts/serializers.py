
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password']

#     def create(self, validated_data):
#         email = validated_data.get('email')
#         first_name = validated_data.get('first_name', '')
#         last_name = validated_data.get('last_name', '')
#         password = validated_data.get('password')

#         # Generate a unique username from email
#         base_username = email.split('@')[0]
#         username = base_username
#         count = 1
#         while User.objects.filter(username=username).exists():
#             username = f"{base_username}{count}"
#             count += 1

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             password=password,
#             is_active=False,  # inactive until email verification
#         )
#         return user

from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        """Ensure the email is unique."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        password = validated_data.get('password')

        # Generate a unique username from email
        base_username = email.split('@')[0]
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=False,  # inactive until email verification
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone', 'address', 'bio', 'image']
