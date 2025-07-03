"""
Serializers for core module.
"""
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import (
    Tag, Note, Attachment, Activity, Dashboard, Widget, Report,
    Workflow, WorkflowExecution, Setting, Notification
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model."""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Note
        fields = [
            'id', 'content', 'is_private', 'content_type', 'object_id',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AttachmentSerializer(serializers.ModelSerializer):
    """Serializer for Attachment model."""
    
    file_size_mb = serializers.ReadOnlyField()
    uploaded_by = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Attachment
        fields = [
            'id', 'name', 'file', 'file_size', 'file_size_mb', 'mime_type',
            'content_type', 'object_id', 'uploaded_by', 'created_at'
        ]
        read_only_fields = ['id', 'file_size', 'mime_type', 'created_at']
    
    def create(self, validated_data):
        """Create attachment with file metadata."""
        file_obj = validated_data['file']
        validated_data['file_size'] = file_obj.size
        validated_data['mime_type'] = getattr(file_obj, 'content_type', 'application/octet-stream')
        return super().create(validated_data)


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'description', 'activity_type', 'status', 'priority',
            'scheduled_date', 'duration_minutes', 'completed_date',
            'assigned_to', 'assigned_to_name', 'content_type', 'object_id',
            'created_by_name', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_date', 'created_at', 'updated_at']
    
    def validate_scheduled_date(self, value):
        """Validate scheduled date is not in the past."""
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Scheduled date cannot be in the past.")
        return value


class WidgetSerializer(serializers.ModelSerializer):
    """Serializer for Widget model."""
    
    class Meta:
        model = Widget
        fields = [
            'id', 'name', 'widget_type', 'config', 'position_x', 'position_y',
            'width', 'height', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardSerializer(serializers.ModelSerializer):
    """Serializer for Dashboard model."""
    
    widgets = WidgetSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'name', 'description', 'is_default', 'is_shared',
            'layout_config', 'widgets', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report model."""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'name', 'description', 'report_type', 'module',
            'config', 'is_shared', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowSerializer(serializers.ModelSerializer):
    """Serializer for Workflow model."""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    execution_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'trigger_model', 'trigger_condition',
            'actions', 'is_active', 'execution_count', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_execution_count(self, obj):
        return obj.executions.count()


class WorkflowExecutionSerializer(serializers.ModelSerializer):
    """Serializer for WorkflowExecution model."""
    
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkflowExecution
        fields = [
            'id', 'workflow', 'workflow_name', 'status', 'trigger_data',
            'execution_log', 'duration', 'started_at', 'completed_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_duration(self, obj):
        if obj.started_at and obj.completed_at:
            delta = obj.completed_at - obj.started_at
            return delta.total_seconds()
        return None


class SettingSerializer(serializers.ModelSerializer):
    """Serializer for Setting model."""
    
    class Meta:
        model = Setting
        fields = ['id', 'key', 'value', 'description', 'is_public', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'is_read',
            'read_at', 'content_type', 'object_id', 'created_by_name',
            'created_at'
        ]
        read_only_fields = ['id', 'read_at', 'created_at']


class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity summary data."""
    
    total_activities = serializers.IntegerField()
    completed_activities = serializers.IntegerField()
    overdue_activities = serializers.IntegerField()
    upcoming_activities = serializers.IntegerField()
    completion_rate = serializers.FloatField()


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_records = serializers.IntegerField()
    recent_activities = ActivitySerializer(many=True)
    unread_notifications = serializers.IntegerField()
    system_health = serializers.DictField()


class GenericRelatedObjectSerializer(serializers.Serializer):
    """Serializer for generic related objects (notes, attachments, activities)."""
    
    notes = NoteSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        """Get related objects for any model instance."""
        from django.contrib.contenttypes.models import ContentType
        
        content_type = ContentType.objects.get_for_model(instance)
        object_id = str(instance.pk)
        
        # Get related objects
        notes = Note.objects.filter(
            content_type=content_type,
            object_id=object_id,
            organization=instance.organization
        ).select_related('created_by')
        
        attachments = Attachment.objects.filter(
            content_type=content_type,
            object_id=object_id,
            organization=instance.organization
        ).select_related('created_by')
        
        activities = Activity.objects.filter(
            content_type=content_type,
            object_id=object_id,
            organization=instance.organization
        ).select_related('assigned_to', 'created_by')
        
        return {
            'notes': NoteSerializer(notes, many=True).data,
            'attachments': AttachmentSerializer(attachments, many=True).data,
            'activities': ActivitySerializer(activities, many=True).data,
        }
