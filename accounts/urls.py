from django.urls import path
from .import views


urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),    
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),

    path('request-reset-password/', views.PasswordResetRequestAPIView.as_view(), name='request-reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmAPIView.as_view(), name='reset-password-confirm'),
    
    path('request-email-change/', views.RequestEmailChangeAPIView.as_view(), name='request-email-change'),
    path('confirm-email-change/<uidb64>/<token>/', views.ConfirmEmailChangeAPIView.as_view(), name='confirm-email-change'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
