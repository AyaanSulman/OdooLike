"""
Admin configuration for authentication module.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Organization, Invitation, UserSession, AuditLog


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin for Organization model."""
    
    list_display = ['name', 'slug', 'plan', 'status', 'user_count', 'created_at']
    list_filter = ['plan', 'status', 'created_at']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'website', 'phone', 'address')
        }),
        ('Subscription', {
            'fields': ('plan', 'status', 'subscription_start', 'subscription_end')
        }),
        ('Limits', {
            'fields': ('max_users', 'max_storage_gb')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for User model."""
    
    list_display = ['email', 'full_name', 'organization', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_verified', 'organization', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['email']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar')
        }),
        ('Organization', {
            'fields': ('organization', 'role', 'job_title', 'department', 'bio')
        }),
        ('Settings', {
            'fields': ('timezone', 'language')
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone')
        }),
        ('Organization', {
            'fields': ('organization', 'role')
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    """Admin for Invitation model."""
    
    list_display = ['email', 'organization', 'role', 'status', 'invited_by', 'created_at']
    list_filter = ['status', 'role', 'organization', 'created_at']
    search_fields = ['email', 'organization__name', 'invited_by__email']
    readonly_fields = ['id', 'token', 'created_at', 'accepted_at']
    
    fieldsets = (
        ('Invitation Details', {
            'fields': ('organization', 'email', 'role', 'invited_by')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'expires_at', 'accepted_at')
        }),
        ('Security', {
            'fields': ('id', 'token'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Admin for UserSession model."""
    
    list_display = ['user', 'ip_address', 'is_active', 'created_at', 'last_activity']
    list_filter = ['is_active', 'created_at', 'last_activity']
    search_fields = ['user__email', 'ip_address', 'session_key']
    readonly_fields = ['id', 'created_at', 'last_activity']
    
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'session_key', 'is_active')
        }),
        ('Client Info', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_activity')
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model."""
    
    list_display = ['user', 'organization', 'action', 'resource_type', 'created_at']
    list_filter = ['action', 'resource_type', 'organization', 'created_at']
    search_fields = ['user__email', 'description', 'resource_id']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Action Details', {
            'fields': ('user', 'organization', 'action', 'resource_type', 'resource_id')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Client Info', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
