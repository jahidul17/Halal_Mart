from django.urls import path
from .import views


urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    
    path('logout/', views.LogoutApiView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirmApiView.as_view(), name='reset-password'),
    
     path('profile/', views.ProfileView.as_view(), name='profile'),
]
