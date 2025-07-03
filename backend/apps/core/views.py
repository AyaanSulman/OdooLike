"""
Views for core module.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import (
    Tag, Note, Attachment, Activity, Dashboard, Widget, Report,
    Workflow, WorkflowExecution, Setting, Notification
)
from .serializers import (
    TagSerializer, NoteSerializer, AttachmentSerializer, ActivitySerializer,
    DashboardSerializer, WidgetSerializer, ReportSerializer,
    WorkflowSerializer, WorkflowExecutionSerializer, SettingSerializer,
    NotificationSerializer, ActivitySummarySerializer, DashboardStatsSerializer,
    GenericRelatedObjectSerializer
)


class TagListCreateView(generics.ListCreateAPIView):
    """List and create tags."""
    
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tag.objects.filter(organization=self.request.user.organization)
    
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user
        )


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete tags."""
    
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tag.objects.filter(organization=self.request.user.organization)


class NoteListCreateView(generics.ListCreateAPIView):
    """List and create notes."""
    
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Note.objects.filter(organization=self.request.user.organization)
        
        # Filter by content type and object id if provided
        content_type_id = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type_id and object_id:
            queryset = queryset.filter(content_type_id=content_type_id, object_id=object_id)
        
        # Filter private notes
        if not self.request.user.has_organization_permission('view_all_notes'):
            queryset = queryset.filter(
                Q(is_private=False) | Q(created_by=self.request.user)
            )
        
        return queryset.select_related('created_by')
    
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user
        )


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete notes."""
    
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Note.objects.filter(organization=self.request.user.organization)
        
        # Filter private notes
        if not self.request.user.has_organization_permission('view_all_notes'):
            queryset = queryset.filter(
                Q(is_private=False) | Q(created_by=self.request.user)
            )
        
        return queryset


class AttachmentListCreateView(generics.ListCreateAPIView):
    """List and create attachments."""
    
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Attachment.objects.filter(organization=self.request.user.organization)
        
        # Filter by content type and object id if provided
        content_type_id = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type_id and object_id:
            queryset = queryset.filter(content_type_id=content_type_id, object_id=object_id)
        
        return queryset.select_related('created_by')
    
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user
        )


class AttachmentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve and delete attachments."""
    
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Attachment.objects.filter(organization=self.request.user.organization)


class ActivityListCreateView(generics.ListCreateAPIView):
    """List and create activities."""
    
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.filter(organization=self.request.user.organization)
        
        # Filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        elif not self.request.user.has_organization_permission('view_all_activities'):
            # Show only user's activities if no permission to view all
            queryset = queryset.filter(assigned_to=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by content type and object id if provided
        content_type_id = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type_id and object_id:
            queryset = queryset.filter(content_type_id=content_type_id, object_id=object_id)
        
        return queryset.select_related('assigned_to', 'created_by')
    
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user
        )


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete activities."""
    
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Activity.objects.filter(organization=self.request.user.organization)
        
        # Users can only modify their own activities unless they have permission
        if not self.request.user.has_organization_permission('manage_all_activities'):
            queryset = queryset.filter(assigned_to=self.request.user)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_activity_view(request, pk):
    """Mark activity as completed."""
    try:
        activity = Activity.objects.get(
            pk=pk,
            organization=request.user.organization
        )
        
        # Check permission
        if (activity.assigned_to != request.user and 
            not request.user.has_organization_permission('manage_all_activities')):
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        activity.mark_completed()
        
        return Response({
            'message': 'Activity marked as completed',
            'activity': ActivitySerializer(activity).data
        })
        
    except Activity.DoesNotExist:
        return Response(
            {'error': 'Activity not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class DashboardListCreateView(generics.ListCreateAPIView):
    """List and create dashboards."""
    
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Dashboard.objects.filter(organization=self.request.user.organization)
        
        # Show shared dashboards and user's own dashboards
        if not self.request.user.has_organization_permission('view_all_dashboards'):
            queryset = queryset.filter(
                Q(is_shared=True) | Q(created_by=self.request.user)
            )
        
        return queryset.prefetch_related('widgets')
    
    def perform_create(self, serializer):
        serializer.save(
            organization=self.request.user.organization,
            created_by=self.request.user
        )


class DashboardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete dashboards."""
    
    serializer_class = DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Dashboard.objects.filter(organization=self.request.user.organization)
        
        # Users can only modify their own dashboards unless they have permission
        if not self.request.user.has_organization_permission('manage_all_dashboards'):
            queryset = queryset.filter(created_by=self.request.user)
        
        return queryset.prefetch_related('widgets')


class NotificationListView(generics.ListAPIView):
    """List user notifications."""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
            organization=self.request.user.organization
        ).select_related('created_by')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read_view(request, pk):
    """Mark notification as read."""
    try:
        notification = Notification.objects.get(
            pk=pk,
            recipient=request.user,
            organization=request.user.organization
        )
        notification.mark_as_read()
        
        return Response({'message': 'Notification marked as read'})
        
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read_view(request):
    """Mark all notifications as read."""
    notifications = Notification.objects.filter(
        recipient=request.user,
        organization=request.user.organization,
        is_read=False
    )
    
    count = notifications.update(is_read=True, read_at=timezone.now())
    
    return Response({'message': f'{count} notifications marked as read'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats_view(request):
    """Get dashboard statistics."""
    org = request.user.organization
    
    # Get basic stats
    total_users = org.users.count()
    active_users = org.users.filter(last_login__gte=timezone.now() - timedelta(days=30)).count()
    
    # Get recent activities
    recent_activities = Activity.objects.filter(
        organization=org,
        created_at__gte=timezone.now() - timedelta(days=7)
    ).select_related('assigned_to', 'created_by')[:10]
    
    # Get unread notifications count
    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        organization=org,
        is_read=False
    ).count()
    
    # System health (placeholder)
    system_health = {
        'status': 'healthy',
        'uptime': '99.9%',
        'response_time': '120ms'
    }
    
    # Total records across modules (placeholder - would be calculated from actual modules)
    total_records = 0
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'total_records': total_records,
        'recent_activities': ActivitySerializer(recent_activities, many=True).data,
        'unread_notifications': unread_notifications,
        'system_health': system_health
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def activity_summary_view(request):
    """Get activity summary for the user."""
    user = request.user
    org = user.organization
    
    # Get activities for the user or all if they have permission
    if user.has_organization_permission('view_all_activities'):
        activities = Activity.objects.filter(organization=org)
    else:
        activities = Activity.objects.filter(organization=org, assigned_to=user)
    
    # Calculate summary
    total_activities = activities.count()
    completed_activities = activities.filter(status='completed').count()
    overdue_activities = activities.filter(
        status__in=['planned', 'in_progress'],
        scheduled_date__lt=timezone.now()
    ).count()
    upcoming_activities = activities.filter(
        status__in=['planned', 'in_progress'],
        scheduled_date__gte=timezone.now(),
        scheduled_date__lte=timezone.now() + timedelta(days=7)
    ).count()
    
    completion_rate = (completed_activities / total_activities * 100) if total_activities > 0 else 0
    
    summary = {
        'total_activities': total_activities,
        'completed_activities': completed_activities,
        'overdue_activities': overdue_activities,
        'upcoming_activities': upcoming_activities,
        'completion_rate': round(completion_rate, 2)
    }
    
    serializer = ActivitySummarySerializer(summary)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def related_objects_view(request):
    """Get related objects (notes, attachments, activities) for any model instance."""
    content_type_id = request.query_params.get('content_type')
    object_id = request.query_params.get('object_id')
    
    if not content_type_id or not object_id:
        return Response(
            {'error': 'content_type and object_id are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        content_type = ContentType.objects.get(id=content_type_id)
        model_class = content_type.model_class()
        
        # Get the object instance
        obj = model_class.objects.get(
            pk=object_id,
            organization=request.user.organization
        )
        
        # Serialize related objects
        serializer = GenericRelatedObjectSerializer()
        data = serializer.to_representation(obj)
        
        return Response(data)
        
    except (ContentType.DoesNotExist, model_class.DoesNotExist):
        return Response(
            {'error': 'Object not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
