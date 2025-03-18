from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    RegisterView,
    LoginView,
    LogoutView,
    ChangePasswordView,
    UpdateUsernameView,
    RequestPasswordResetView,
    ResetPasswordView,
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Password management
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # Profile management
    path('update-username/', UpdateUsernameView.as_view(), name='update-username'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]