"""
Core models for the ERP system.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )
    organization = models.ForeignKey(
        'authentication.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )
    
    class Meta:
        abstract = True


class Tag(BaseModel):
    """Tag model for categorizing records."""
    
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'core_tags'
        unique_together = ['name', 'organization']
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Note(BaseModel):
    """Note model for adding notes to any record."""
    
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    
    # Generic foreign key to attach notes to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'core_notes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"Note by {self.created_by} on {self.created_at}"


class Attachment(BaseModel):
    """Attachment model for file uploads."""
    
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    
    # Generic foreign key to attach files to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'core_attachments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)


class Activity(BaseModel):
    """Activity model for tracking actions and events."""
    
    ACTIVITY_TYPES = [
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('task', 'Task'),
        ('note', 'Note'),
        ('deadline', 'Deadline'),
        ('follow_up', 'Follow Up'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='assigned_activities'
    )
    
    # Generic foreign key to link activities to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=100)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'core_activities'
        ordering = ['scheduled_date']
        indexes = [
            models.Index(fields=['assigned_to', 'scheduled_date']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['status', 'scheduled_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_date}"
    
    @property
    def is_overdue(self):
        return (
            self.status in ['planned', 'in_progress'] and 
            self.scheduled_date < timezone.now()
        )
    
    def mark_completed(self):
        self.status = 'completed'
        self.completed_date = timezone.now()
        self.save()


class Dashboard(BaseModel):
    """Dashboard model for custom dashboards."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    layout_config = models.JSONField(default=dict)  # Store dashboard layout
    
    class Meta:
        db_table = 'core_dashboards'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Widget(BaseModel):
    """Widget model for dashboard widgets."""
    
    WIDGET_TYPES = [
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('calendar', 'Calendar'),
        ('kanban', 'Kanban'),
        ('list', 'List'),
    ]
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    name = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    config = models.JSONField(default=dict)  # Widget configuration
    position_x = models.PositiveIntegerField(default=0)
    position_y = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=4)
    height = models.PositiveIntegerField(default=3)
    
    class Meta:
        db_table = 'core_widgets'
        ordering = ['position_y', 'position_x']
    
    def __str__(self):
        return f"{self.name} ({self.widget_type})"


class Report(BaseModel):
    """Report model for custom reports."""
    
    REPORT_TYPES = [
        ('table', 'Table Report'),
        ('chart', 'Chart Report'),
        ('pivot', 'Pivot Table'),
        ('dashboard', 'Dashboard Report'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    module = models.CharField(max_length=50)  # e.g., 'crm', 'inventory', 'accounting'
    config = models.JSONField(default=dict)  # Report configuration
    is_shared = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'core_reports'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Workflow(BaseModel):
    """Workflow model for business process automation."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    trigger_model = models.CharField(max_length=100)  # Model that triggers the workflow
    trigger_condition = models.JSONField(default=dict)  # Conditions to trigger
    actions = models.JSONField(default=list)  # List of actions to perform
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'core_workflows'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class WorkflowExecution(BaseModel):
    """Track workflow executions."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    trigger_data = models.JSONField(default=dict)
    execution_log = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'core_workflow_executions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.status}"


class Setting(BaseModel):
    """Settings model for organization-specific settings."""
    
    key = models.CharField(max_length=100)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)  # Can be accessed by all users
    
    class Meta:
        db_table = 'core_settings'
        unique_together = ['organization', 'key']
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value}"


class Notification(BaseModel):
    """Notification model for user notifications."""
    
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    
    recipient = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Optional link to related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        db_table = 'core_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.email}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class SystemLog(models.Model):
    """System log for tracking system events."""
    
    LOG_LEVELS = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.CharField(max_length=20, choices=LOG_LEVELS)
    message = models.TextField()
    module = models.CharField(max_length=100)
    function = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    organization = models.ForeignKey(
        'authentication.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    extra_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'core_system_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['module', 'created_at']),
        ]
    
    def __str__(self):
        return f"[{self.level.upper()}] {self.message[:50]}"
