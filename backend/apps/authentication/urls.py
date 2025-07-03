"""
URL configuration for authentication module.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('permissions/', views.user_permissions_view, name='user_permissions'),
    
    # Organization
    path('organization/', views.OrganizationView.as_view(), name='organization'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    
    # Invitations
    path('invitations/', views.InvitationListCreateView.as_view(), name='invitation_list_create'),
    path('invitations/<uuid:token>/accept/', views.accept_invitation_view, name='accept_invitation'),
]
