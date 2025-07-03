"""
Views for CRM module.
"""
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Contact, Lead, Opportunity, Campaign, SalesStage, EmailTemplate
from .serializers import (
    ContactSerializer, ContactListSerializer, LeadSerializer, LeadListSerializer,
    OpportunitySerializer, OpportunityListSerializer, CampaignSerializer,
    SalesStageSerializer, EmailTemplateSerializer, LeadConversionSerializer,
    OpportunityStageUpdateSerializer, CRMStatsSerializer, SalesPipelineSerializer
)


class ContactListCreateView(generics.ListCreateAPIView):
    """List and create contacts."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contact_type', 'is_active', 'industry']
    search_fields = ['first_name', 'last_name', 'company_name', 'email', 'phone']
    ordering_fields = ['first_name', 'last_name', 'company_name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Contact.objects.filter(organization=self.request.user.organization)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactListSerializer
        return ContactSerializer


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete contact."""
    
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Contact.objects.filter(organization=self.request.user.organization)


class LeadListCreateView(generics.ListCreateAPIView):
    """List and create leads."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'source', 'assigned_to']
    search_fields = ['title', 'contact_name', 'company_name', 'email']
    ordering_fields = ['title', 'contact_name', 'estimated_value', 'expected_close_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Lead.objects.filter(organization=self.request.user.organization)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LeadListSerializer
        return LeadSerializer


class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete lead."""
    
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Lead.objects.filter(organization=self.request.user.organization)


class OpportunityListCreateView(generics.ListCreateAPIView):
    """List and create opportunities."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stage', 'priority', 'assigned_to', 'contact']
    search_fields = ['name', 'description', 'contact__first_name', 'contact__last_name', 'contact__company_name']
    ordering_fields = ['name', 'estimated_value', 'probability', 'expected_close_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Opportunity.objects.filter(organization=self.request.user.organization).select_related('contact', 'assigned_to')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OpportunityListSerializer
        return OpportunitySerializer


class OpportunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete opportunity."""
    
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Opportunity.objects.filter(organization=self.request.user.organization).select_related('contact', 'assigned_to')


class CampaignListCreateView(generics.ListCreateAPIView):
    """List and create campaigns."""
    
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['campaign_type', 'status', 'assigned_to']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'start_date', 'end_date', 'budget', 'created_at']
    ordering = ['-start_date']
    
    def get_queryset(self):
        return Campaign.objects.filter(organization=self.request.user.organization)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete campaign."""
    
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Campaign.objects.filter(organization=self.request.user.organization)


class SalesStageListCreateView(generics.ListCreateAPIView):
    """List and create sales stages."""
    
    serializer_class = SalesStageSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['order']
    
    def get_queryset(self):
        return SalesStage.objects.filter(organization=self.request.user.organization)


class SalesStageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete sales stage."""
    
    serializer_class = SalesStageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SalesStage.objects.filter(organization=self.request.user.organization)


class EmailTemplateListCreateView(generics.ListCreateAPIView):
    """List and create email templates."""
    
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['template_type', 'is_active']
    search_fields = ['name', 'subject']
    
    def get_queryset(self):
        return EmailTemplate.objects.filter(organization=self.request.user.organization)


class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete email template."""
    
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return EmailTemplate.objects.filter(organization=self.request.user.organization)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_lead_view(request, pk):
    """Convert lead to contact and opportunity."""
    
    lead = get_object_or_404(Lead, pk=pk, organization=request.user.organization)
    
    if lead.is_converted:
        return Response(
            {'error': 'Lead has already been converted'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = LeadConversionSerializer(data=request.data)
    if serializer.is_valid():
        contact, opportunity = lead.convert_to_contact_and_opportunity(request.user)
        
        return Response({
            'message': 'Lead converted successfully',
            'contact_id': str(contact.id),
            'opportunity_id': str(opportunity.id) if opportunity else None
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_opportunity_stage_view(request, pk):
    """Update opportunity stage."""
    
    opportunity = get_object_or_404(Opportunity, pk=pk, organization=request.user.organization)
    
    serializer = OpportunityStageUpdateSerializer(data=request.data)
    if serializer.is_valid():
        stage = serializer.validated_data['stage']
        reason = serializer.validated_data.get('reason', '')
        
        if stage == 'closed_won':
            opportunity.close_as_won(request.user)
        elif stage == 'closed_lost':
            opportunity.close_as_lost(request.user, reason)
        else:
            opportunity.stage = stage
            opportunity.updated_by = request.user
            opportunity.save()
        
        return Response({
            'message': 'Opportunity stage updated successfully',
            'stage': opportunity.stage
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crm_stats_view(request):
    """Get CRM statistics."""
    
    organization = request.user.organization
    
    # Basic counts
    total_contacts = Contact.objects.filter(organization=organization, is_active=True).count()
    total_leads = Lead.objects.filter(organization=organization).count()
    total_opportunities = Opportunity.objects.filter(organization=organization).count()
    total_campaigns = Campaign.objects.filter(organization=organization).count()
    
    # Leads by status
    leads_by_status = dict(
        Lead.objects.filter(organization=organization)
        .values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )
    
    # Opportunities by stage
    opportunities_by_stage = dict(
        Opportunity.objects.filter(organization=organization)
        .values('stage')
        .annotate(count=Count('id'))
        .values_list('stage', 'count')
    )
    
    # Pipeline values
    pipeline_stats = Opportunity.objects.filter(
        organization=organization,
        stage__in=['qualification', 'needs_analysis', 'proposal', 'negotiation']
    ).aggregate(
        total_value=Sum('estimated_value'),
        weighted_value=Sum('estimated_value') * Sum('probability') / 100 if Sum('probability') else 0
    )
    
    # Won opportunities
    won_stats = Opportunity.objects.filter(
        organization=organization,
        stage='closed_won'
    ).aggregate(
        count=Count('id'),
        total_value=Sum('estimated_value')
    )
    
    # Conversion rate (leads to opportunities)
    converted_leads = Lead.objects.filter(organization=organization, converted_opportunity__isnull=False).count()
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    # Average deal size
    average_deal_size = won_stats['total_value'] / won_stats['count'] if won_stats['count'] > 0 else 0
    
    stats = {
        'total_contacts': total_contacts,
        'total_leads': total_leads,
        'total_opportunities': total_opportunities,
        'total_campaigns': total_campaigns,
        'leads_by_status': leads_by_status,
        'opportunities_by_stage': opportunities_by_stage,
        'total_pipeline_value': pipeline_stats['total_value'] or 0,
        'weighted_pipeline_value': pipeline_stats['weighted_value'] or 0,
        'won_opportunities_count': won_stats['count'] or 0,
        'won_opportunities_value': won_stats['total_value'] or 0,
        'conversion_rate': conversion_rate,
        'average_deal_size': average_deal_size
    }
    
    serializer = CRMStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_pipeline_view(request):
    """Get sales pipeline data."""
    
    organization = request.user.organization
    
    pipeline_data = []
    stages = ['qualification', 'needs_analysis', 'proposal', 'negotiation']
    
    for stage in stages:
        opportunities = Opportunity.objects.filter(
            organization=organization,
            stage=stage
        ).select_related('contact', 'assigned_to')
        
        stage_data = {
            'stage': stage,
            'count': opportunities.count(),
            'total_value': sum(opp.estimated_value for opp in opportunities),
            'weighted_value': sum(opp.weighted_value for opp in opportunities),
            'opportunities': OpportunityListSerializer(opportunities, many=True).data
        }
        pipeline_data.append(stage_data)
    
    serializer = SalesPipelineSerializer(pipeline_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_leads_view(request):
    """Get leads assigned to current user."""
    
    leads = Lead.objects.filter(
        organization=request.user.organization,
        assigned_to=request.user
    ).order_by('-created_at')
    
    serializer = LeadListSerializer(leads, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_opportunities_view(request):
    """Get opportunities assigned to current user."""
    
    opportunities = Opportunity.objects.filter(
        organization=request.user.organization,
        assigned_to=request.user
    ).select_related('contact').order_by('-created_at')
    
    serializer = OpportunityListSerializer(opportunities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overdue_activities_view(request):
    """Get overdue activities for CRM objects."""
    
    from apps.core.models import Activity
    from django.contrib.contenttypes.models import ContentType
    
    # Get content types for CRM models
    lead_ct = ContentType.objects.get_for_model(Lead)
    opportunity_ct = ContentType.objects.get_for_model(Opportunity)
    contact_ct = ContentType.objects.get_for_model(Contact)
    
    overdue_activities = Activity.objects.filter(
        organization=request.user.organization,
        status='pending',
        scheduled_date__lt=timezone.now().date(),
        content_type__in=[lead_ct, opportunity_ct, contact_ct]
    ).select_related('assigned_to').order_by('scheduled_date')
    
    from apps.core.serializers import ActivitySerializer
    serializer = ActivitySerializer(overdue_activities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_activities_view(request):
    """Get recent activities for CRM objects."""
    
    from apps.core.models import Activity
    from django.contrib.contenttypes.models import ContentType
    
    # Get content types for CRM models
    lead_ct = ContentType.objects.get_for_model(Lead)
    opportunity_ct = ContentType.objects.get_for_model(Opportunity)
    contact_ct = ContentType.objects.get_for_model(Contact)
    
    recent_activities = Activity.objects.filter(
        organization=request.user.organization,
        content_type__in=[lead_ct, opportunity_ct, contact_ct]
    ).select_related('assigned_to').order_by('-created_at')[:20]
    
    from apps.core.serializers import ActivitySerializer
    serializer = ActivitySerializer(recent_activities, many=True)
    return Response(serializer.data)
