from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .utils import get_tokens_for_user
from .tokens import generate_token  
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.utils.encoding import force_str 
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics, permissions
from .serializers import ProfileSerializer
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class RegisterApiView(APIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            email_subject = "Activate Your Account"
            message = render_to_string('activate.html', {
                'user': user,
                'domain': 'http://127.0.0.1:8000',  # change in production
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user),
            })

            try:
                email_message = EmailMultiAlternatives(
                    email_subject, message, to=[user.email]
                )
                email_message.attach_alternative(message, "text/html")
                email_message.send()
            except Exception as e:
                logger.error(f"Email sending failed for {user.email}: {e}")
                # Don't stop registration — just warn the user
                return Response({
                    "message": "Account created, but email sending failed. Please contact support.",
                    "tokens": tokens
                }, status=status.HTTP_201_CREATED)

            return Response({
                "message": "Account created successfully. Check your email to activate your account.",
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterApiView(APIView):
#     serializer_class = serializers.RegisterSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             tokens = get_tokens_for_user(user)

#             email_subject = "Activate Your Account"
#             message = render_to_string('activate.html', {
#                 'user': user,
#                 'domain': 'http://127.0.0.1:8000',
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': generate_token.make_token(user),
#             })
#             email_message = EmailMultiAlternatives(email_subject, message, to=[user.email])
#             email_message.attach_alternative(message, "text/html")
#             email_message.send()

#             return Response({
#                 "message": "Check your email for confirmation.",
#                 "tokens": tokens
#             }, status=201)

#         return Response(serializer.errors, status=400)

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login') 
        else:
            return redirect('register') 



class LoginApiView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({"error": "Please provide both email and password."}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials."}, status=401)

        user = authenticate(username=user.username, password=password)

        if not user:
            return Response({"error": "Invalid credentials."}, status=401)

        tokens = get_tokens_for_user(user)
        return Response({
            "message": "Login successful.",
            "tokens": tokens
        }, status=200)



class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=200)




class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=400)

        if not User.objects.filter(email=email).exists():
            return Response({"error": "No user with this email."}, status=404)

        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://127.0.0.1:8000/api/accounts/reset-password-confirm/{uid}/{token}/"

        subject = "Reset Your Password"
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_url': reset_url
        })

        email_message = EmailMultiAlternatives(subject, message, to=[email])
        email_message.attach_alternative(message, "text/html")
        email_message.send()

        return Response({"message": "Password reset email sent."}, status=200)




class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({"error": "New password is required."}, status=400)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful."}, status=200)
        else:
            return Response({"error": "Invalid or expired token."}, status=400)
        



class RequestEmailChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        new_email = request.data.get('email')

        if not new_email:
            return Response({"error": "New email is required."}, status=400)

        # Check if email already used by someone else
        if User.objects.filter(email=new_email).exists():
            return Response({"error": "This email is already in use."}, status=400)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirm_url = f"http://127.0.0.1:8000/api/accounts/confirm-email-change/{uid}/{token}/?new_email={new_email}"

        # Email context for templates
        context = {
            'user': user,
            'confirm_url': confirm_url,
            'new_email': new_email
        }

        subject = "Confirm Your New Email Address"
        # text_message = render_to_string('email_change_request.txt', context)
        html_message = render_to_string('email_change_request.html', context)

        email_message = EmailMultiAlternatives(subject, html_message, to=[new_email])
        email_message.attach_alternative(html_message, "text/html")
        email_message.send()

        return Response({"message": "Verification email sent to new address."}, status=200)




class ConfirmEmailChangeAPIView(APIView):
    def get(self, request, uidb64, token):
        new_email = request.GET.get('new_email')

        if not new_email:
            return Response({"error": "Missing new_email parameter."}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user."}, status=400)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=400)

        user.email = new_email
        user.save()
        return Response({"message": "Email updated successfully."}, status=200)




class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the authenticated user's profile only
        return self.request.user.profile


