"""
Views for authentication module.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.utils import timezone
from django.db import transaction
from .models import User, Organization, Invitation, AuditLog
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    PasswordChangeSerializer, InvitationSerializer, ProfileSerializer,
    OrganizationSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration view."""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create user and return tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            user = serializer.save()
            
            # Create audit log
            AuditLog.objects.create(
                user=user,
                organization=user.organization,
                action='create',
                resource_type='user',
                resource_id=str(user.id),
                description=f"User {user.email} registered",
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login view."""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    
    # Update last login info
    user.last_login = timezone.now()
    user.last_login_ip = get_client_ip(request)
    user.save(update_fields=['last_login', 'last_login_ip'])
    
    # Create audit log
    if user.organization:
        AuditLog.objects.create(
            user=user,
            organization=user.organization,
            action='login',
            resource_type='user',
            resource_id=str(user.id),
            description=f"User {user.email} logged in",
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout view."""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        # Create audit log
        if request.user.organization:
            AuditLog.objects.create(
                user=request.user,
                organization=request.user.organization,
                action='logout',
                resource_type='user',
                resource_id=str(request.user.id),
                description=f"User {request.user.email} logged out",
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile view."""
    
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """Password change view."""
    
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Create audit log
        if request.user.organization:
            AuditLog.objects.create(
                user=request.user,
                organization=request.user.organization,
                action='update',
                resource_type='user',
                resource_id=str(request.user.id),
                description=f"User {request.user.email} changed password",
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return Response({'message': 'Password changed successfully'})


class OrganizationView(generics.RetrieveUpdateAPIView):
    """Organization view."""
    
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.organization
    
    def update(self, request, *args, **kwargs):
        """Update organization with permission check."""
        if not request.user.has_organization_permission('manage_settings'):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        response = super().update(request, *args, **kwargs)
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user,
            organization=request.user.organization,
            action='update',
            resource_type='organization',
            resource_id=str(request.user.organization.id),
            description=f"Organization {request.user.organization.name} updated",
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return response


class UserListView(generics.ListAPIView):
    """List organization users."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.has_organization_permission('view_users'):
            return User.objects.none()
        
        return User.objects.filter(
            organization=self.request.user.organization
        ).select_related('organization')


class InvitationListCreateView(generics.ListCreateAPIView):
    """List and create invitations."""
    
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.has_organization_permission('manage_users'):
            return Invitation.objects.none()
        
        return Invitation.objects.filter(
            organization=self.request.user.organization
        ).select_related('invited_by', 'organization')
    
    def perform_create(self, serializer):
        """Create invitation with permission check."""
        if not self.request.user.has_organization_permission('manage_users'):
            raise permissions.PermissionDenied("Permission denied")
        
        # Check user limit
        org = self.request.user.organization
        if org.users.count() >= org.max_users:
            raise serializers.ValidationError("User limit reached for your plan")
        
        invitation = serializer.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=self.request.user,
            organization=self.request.user.organization,
            action='create',
            resource_type='invitation',
            resource_id=str(invitation.id),
            description=f"Invitation sent to {invitation.email}",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        # TODO: Send invitation email
        # send_invitation_email.delay(invitation.id)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def accept_invitation_view(request, token):
    """Accept invitation view."""
    try:
        invitation = Invitation.objects.get(token=token, status='pending')
        
        if invitation.is_expired:
            return Response(
                {'error': 'Invitation has expired'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Return invitation details for registration
        return Response({
            'invitation': InvitationSerializer(invitation).data,
            'organization': OrganizationSerializer(invitation.organization).data
        })
        
    except Invitation.DoesNotExist:
        return Response(
            {'error': 'Invalid invitation token'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions_view(request):
    """Get user permissions."""
    user = request.user
    
    permissions_map = {
        'owner': {
            'manage_users': True,
            'manage_settings': True,
            'view_reports': True,
            'manage_data': True,
            'view_data': True,
            'export_data': True,
        },
        'admin': {
            'manage_users': True,
            'manage_settings': True,
            'view_reports': True,
            'manage_data': True,
            'view_data': True,
            'export_data': True,
        },
        'manager': {
            'manage_users': False,
            'manage_settings': False,
            'view_reports': True,
            'manage_data': True,
            'view_data': True,
            'export_data': True,
        },
        'employee': {
            'manage_users': False,
            'manage_settings': False,
            'view_reports': False,
            'manage_data': True,
            'view_data': True,
            'export_data': False,
        },
        'viewer': {
            'manage_users': False,
            'manage_settings': False,
            'view_reports': False,
            'manage_data': False,
            'view_data': True,
            'export_data': False,
        },
    }
    
    user_permissions = permissions_map.get(user.role, {})
    
    return Response({
        'user': UserSerializer(user).data,
        'permissions': user_permissions,
        'organization': OrganizationSerializer(user.organization).data if user.organization else None
    })


def get_client_ip(request):
    """Helper function to get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
