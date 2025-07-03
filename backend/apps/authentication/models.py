"""
Authentication models for the business management SaaS platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class Organization(models.Model):
    """Organization model for multi-tenant SaaS architecture."""
    
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Subscription details
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    subscription_start = models.DateTimeField(default=timezone.now)
    subscription_end = models.DateTimeField(null=True, blank=True)
    
    # Limits based on plan
    max_users = models.IntegerField(default=5)
    max_storage_gb = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_subscription_valid(self):
        if not self.subscription_end:
            return True
        return timezone.now() <= self.subscription_end


class User(AbstractUser):
    """Extended User model with organization support."""
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('viewer', 'Viewer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Organization relationship
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='users',
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    
    # Profile information
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    
    # Settings
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Status
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def has_organization_permission(self, permission):
        """Check if user has specific organization permission."""
        role_permissions = {
            'owner': ['all'],
            'admin': ['manage_users', 'manage_settings', 'view_reports', 'manage_data'],
            'manager': ['view_reports', 'manage_data', 'view_users'],
            'employee': ['manage_data'],
            'viewer': ['view_data'],
        }
        
        user_permissions = role_permissions.get(self.role, [])
        return 'all' in user_permissions or permission in user_permissions


class Invitation(models.Model):
    """Model for inviting users to organizations."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES, default='employee')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'invitations'
        unique_together = ['organization', 'email']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Invitation to {self.email} for {self.organization.name}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def accept(self, user):
        """Accept the invitation and add user to organization."""
        if self.is_expired or self.status != 'pending':
            return False
        
        user.organization = self.organization
        user.role = self.role
        user.save()
        
        self.status = 'accepted'
        self.accepted_at = timezone.now()
        self.save()
        
        return True


class UserSession(models.Model):
    """Track user sessions for security and analytics."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"Session for {self.user.email} from {self.ip_address}"


class AuditLog(models.Model):
    """Audit log for tracking user actions."""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('export', 'Export'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='audit_logs')
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=50)  # e.g., 'contact', 'product', 'invoice'
    resource_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]
    
    def __str__(self):
        return f"{self.user} {self.action} {self.resource_type} at {self.created_at}"
