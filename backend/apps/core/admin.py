"""
Admin configuration for core module.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Tag, Note, Attachment, Activity, Dashboard, Widget, Report,
    Workflow, WorkflowExecution, Setting, Notification, SystemLog
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag model."""
    
    list_display = ['name', 'color_display', 'organization', 'created_at']
    list_filter = ['organization', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 2px 8px; border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin for Note model."""
    
    list_display = ['content_preview', 'created_by', 'organization', 'is_private', 'created_at']
    list_filter = ['is_private', 'organization', 'created_at']
    search_fields = ['content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Admin for Attachment model."""
    
    list_display = ['name', 'file_size_mb', 'mime_type', 'created_by', 'organization', 'created_at']
    list_filter = ['mime_type', 'organization', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'file_size', 'mime_type', 'created_at', 'updated_at']
    
    def file_size_mb(self, obj):
        return f"{obj.file_size_mb} MB"
    file_size_mb.short_description = 'File Size'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin for Activity model."""
    
    list_display = ['title', 'activity_type', 'status', 'priority', 'assigned_to', 'scheduled_date', 'is_overdue']
    list_filter = ['activity_type', 'status', 'priority', 'organization', 'scheduled_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'is_overdue', 'completed_date', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'


class WidgetInline(admin.TabularInline):
    """Inline admin for Widget model."""
    model = Widget
    extra = 0
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    """Admin for Dashboard model."""
    
    list_display = ['name', 'is_default', 'is_shared', 'created_by', 'organization', 'created_at']
    list_filter = ['is_default', 'is_shared', 'organization', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [WidgetInline]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin for Report model."""
    
    list_display = ['name', 'report_type', 'module', 'is_shared', 'created_by', 'organization', 'created_at']
    list_filter = ['report_type', 'module', 'is_shared', 'organization', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


class WorkflowExecutionInline(admin.TabularInline):
    """Inline admin for WorkflowExecution model."""
    model = WorkflowExecution
    extra = 0
    readonly_fields = ['id', 'status', 'started_at', 'completed_at', 'created_at']


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    """Admin for Workflow model."""
    
    list_display = ['name', 'trigger_model', 'is_active', 'execution_count', 'created_by', 'organization', 'created_at']
    list_filter = ['is_active', 'trigger_model', 'organization', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [WorkflowExecutionInline]
    
    def execution_count(self, obj):
        return obj.executions.count()
    execution_count.short_description = 'Executions'


@admin.register(WorkflowExecution)
class WorkflowExecutionAdmin(admin.ModelAdmin):
    """Admin for WorkflowExecution model."""
    
    list_display = ['workflow', 'status', 'started_at', 'completed_at', 'duration', 'created_at']
    list_filter = ['status', 'workflow', 'created_at']
    readonly_fields = ['id', 'duration', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def duration(self, obj):
        if obj.started_at and obj.completed_at:
            delta = obj.completed_at - obj.started_at
            return f"{delta.total_seconds():.2f}s"
        return "N/A"
    duration.short_description = 'Duration'


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin for Setting model."""
    
    list_display = ['key', 'value_preview', 'is_public', 'organization', 'created_at']
    list_filter = ['is_public', 'organization', 'created_at']
    search_fields = ['key', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def value_preview(self, obj):
        value_str = str(obj.value)
        return value_str[:50] + '...' if len(value_str) > 50 else value_str
    value_preview.short_description = 'Value'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin for Notification model."""
    
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'organization', 'created_at']
    search_fields = ['title', 'message', 'recipient__email']
    readonly_fields = ['id', 'read_at', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    """Admin for SystemLog model."""
    
    list_display = ['level', 'message_preview', 'module', 'user', 'created_at']
    list_filter = ['level', 'module', 'created_at']
    search_fields = ['message', 'module', 'function']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
