"""
URL configuration for core module.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Tags
    path('tags/', views.TagListCreateView.as_view(), name='tag_list_create'),
    path('tags/<uuid:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # Notes
    path('notes/', views.NoteListCreateView.as_view(), name='note_list_create'),
    path('notes/<uuid:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    
    # Attachments
    path('attachments/', views.AttachmentListCreateView.as_view(), name='attachment_list_create'),
    path('attachments/<uuid:pk>/', views.AttachmentDetailView.as_view(), name='attachment_detail'),
    
    # Activities
    path('activities/', views.ActivityListCreateView.as_view(), name='activity_list_create'),
    path('activities/<uuid:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<uuid:pk>/complete/', views.complete_activity_view, name='complete_activity'),
    path('activities/summary/', views.activity_summary_view, name='activity_summary'),
    
    # Dashboards
    path('dashboards/', views.DashboardListCreateView.as_view(), name='dashboard_list_create'),
    path('dashboards/<uuid:pk>/', views.DashboardDetailView.as_view(), name='dashboard_detail'),
    
    # Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<uuid:pk>/read/', views.mark_notification_read_view, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read_view, name='mark_all_notifications_read'),
    
    # Dashboard and Statistics
    path('dashboard/stats/', views.dashboard_stats_view, name='dashboard_stats'),
    
    # Related Objects
    path('related-objects/', views.related_objects_view, name='related_objects'),
]
