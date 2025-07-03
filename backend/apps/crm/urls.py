"""
URL configuration for CRM module.
"""
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Contacts
    path('contacts/', views.ContactListCreateView.as_view(), name='contact_list_create'),
    path('contacts/<uuid:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    
    # Leads
    path('leads/', views.LeadListCreateView.as_view(), name='lead_list_create'),
    path('leads/<uuid:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('leads/<uuid:pk>/convert/', views.convert_lead_view, name='convert_lead'),
    path('leads/my/', views.my_leads_view, name='my_leads'),
    
    # Opportunities
    path('opportunities/', views.OpportunityListCreateView.as_view(), name='opportunity_list_create'),
    path('opportunities/<uuid:pk>/', views.OpportunityDetailView.as_view(), name='opportunity_detail'),
    path('opportunities/<uuid:pk>/stage/', views.update_opportunity_stage_view, name='update_opportunity_stage'),
    path('opportunities/my/', views.my_opportunities_view, name='my_opportunities'),
    
    # Campaigns
    path('campaigns/', views.CampaignListCreateView.as_view(), name='campaign_list_create'),
    path('campaigns/<uuid:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    
    # Sales Stages
    path('sales-stages/', views.SalesStageListCreateView.as_view(), name='sales_stage_list_create'),
    path('sales-stages/<uuid:pk>/', views.SalesStageDetailView.as_view(), name='sales_stage_detail'),
    
    # Email Templates
    path('email-templates/', views.EmailTemplateListCreateView.as_view(), name='email_template_list_create'),
    path('email-templates/<uuid:pk>/', views.EmailTemplateDetailView.as_view(), name='email_template_detail'),
    
    # Analytics and Reports
    path('stats/', views.crm_stats_view, name='crm_stats'),
    path('pipeline/', views.sales_pipeline_view, name='sales_pipeline'),
    path('activities/overdue/', views.overdue_activities_view, name='overdue_activities'),
    path('activities/recent/', views.recent_activities_view, name='recent_activities'),
]
