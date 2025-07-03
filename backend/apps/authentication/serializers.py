"""
Serializers for authentication module.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta
from .models import User, Organization, Invitation


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model."""
    
    user_count = serializers.SerializerMethodField()
    is_subscription_valid = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'slug', 'description', 'website', 'phone', 'address',
            'plan', 'status', 'subscription_start', 'subscription_end',
            'max_users', 'max_storage_gb', 'user_count', 'is_subscription_valid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_count(self, obj):
        return obj.users.count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    full_name = serializers.ReadOnlyField()
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar', 'organization', 'organization_name', 'role',
            'job_title', 'department', 'bio', 'timezone', 'language',
            'is_verified', 'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    organization_name = serializers.CharField(write_only=True, required=False)
    invitation_token = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'organization_name',
            'invitation_token'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation and invitation token."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        
        # Check invitation token if provided
        if 'invitation_token' in attrs:
            try:
                invitation = Invitation.objects.get(
                    token=attrs['invitation_token'],
                    status='pending',
                    email=attrs['email']
                )
                if invitation.is_expired:
                    raise serializers.ValidationError("Invitation has expired.")
                attrs['invitation'] = invitation
            except Invitation.DoesNotExist:
                raise serializers.ValidationError("Invalid invitation token.")
        
        return attrs
    
    def create(self, validated_data):
        """Create user and handle organization assignment."""
        validated_data.pop('password_confirm')
        organization_name = validated_data.pop('organization_name', None)
        invitation = validated_data.pop('invitation', None)
        
        user = User.objects.create_user(**validated_data)
        
        if invitation:
            # Accept invitation
            invitation.accept(user)
        elif organization_name:
            # Create new organization
            from django.utils.text import slugify
            organization = Organization.objects.create(
                name=organization_name,
                slug=slugify(organization_name)
            )
            user.organization = organization
            user.role = 'owner'
            user.save()
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            if user.organization and not user.organization.is_active:
                raise serializers.ValidationError("Organization account is suspended.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password.")


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, attrs):
        """Validate new password confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def save(self):
        """Change user password."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class InvitationSerializer(serializers.ModelSerializer):
    """Serializer for Invitation model."""
    
    invited_by_name = serializers.CharField(source='invited_by.full_name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Invitation
        fields = [
            'id', 'email', 'role', 'status', 'token',
            'invited_by_name', 'organization_name', 'is_expired',
            'created_at', 'expires_at', 'accepted_at'
        ]
        read_only_fields = ['id', 'token', 'status', 'created_at', 'expires_at', 'accepted_at']
    
    def create(self, validated_data):
        """Create invitation with expiration date."""
        validated_data['invited_by'] = self.context['request'].user
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['expires_at'] = timezone.now() + timedelta(days=7)
        return super().create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'avatar',
            'job_title', 'department', 'bio', 'timezone', 'language'
        ]
    
    def update(self, instance, validated_data):
        """Update user profile."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
