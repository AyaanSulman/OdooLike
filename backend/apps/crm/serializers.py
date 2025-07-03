"""
Serializers for CRM module.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact, Lead, Opportunity, Campaign, SalesStage, EmailTemplate

User = get_user_model()


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Contact
        fields = [
            'id', 'contact_type', 'salutation', 'first_name', 'last_name', 
            'company_name', 'job_title', 'email', 'phone', 'mobile', 'website',
            'street_address', 'city', 'state', 'postal_code', 'country',
            'industry', 'annual_revenue', 'employee_count', 'parent_contact',
            'linkedin_url', 'twitter_handle', 'facebook_url', 'is_active',
            'tags', 'source', 'description', 'full_name', 'display_name',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'display_name']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ContactListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Contact list views."""
    
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Contact
        fields = [
            'id', 'contact_type', 'first_name', 'last_name', 'company_name',
            'email', 'phone', 'city', 'country', 'is_active', 'full_name',
            'display_name', 'created_at'
        ]


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model."""
    
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_converted = serializers.ReadOnlyField()
    converted_contact_name = serializers.CharField(source='converted_contact.display_name', read_only=True)
    converted_opportunity_name = serializers.CharField(source='converted_opportunity.name', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'title', 'description', 'contact_name', 'company_name',
            'email', 'phone', 'status', 'priority', 'source', 'estimated_value',
            'probability', 'assigned_to', 'expected_close_date', 'converted_contact',
            'converted_opportunity', 'converted_at', 'tags', 'assigned_to_name',
            'created_by_name', 'is_converted', 'converted_contact_name',
            'converted_opportunity_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'converted_contact', 'converted_opportunity', 'converted_at',
            'is_converted', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class LeadListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Lead list views."""
    
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    is_converted = serializers.ReadOnlyField()
    
    class Meta:
        model = Lead
        fields = [
            'id', 'title', 'contact_name', 'company_name', 'email',
            'status', 'priority', 'estimated_value', 'probability',
            'assigned_to_name', 'expected_close_date', 'is_converted',
            'created_at'
        ]


class OpportunitySerializer(serializers.ModelSerializer):
    """Serializer for Opportunity model."""
    
    contact_name = serializers.CharField(source='contact.display_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_closed = serializers.ReadOnlyField()
    is_won = serializers.ReadOnlyField()
    weighted_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Opportunity
        fields = [
            'id', 'name', 'description', 'contact', 'stage', 'priority',
            'estimated_value', 'probability', 'assigned_to', 'expected_close_date',
            'actual_close_date', 'competitors', 'lead_source', 'tags',
            'contact_name', 'assigned_to_name', 'created_by_name', 'is_closed',
            'is_won', 'weighted_value', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'actual_close_date', 'is_closed', 'is_won', 'weighted_value', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class OpportunityListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Opportunity list views."""
    
    contact_name = serializers.CharField(source='contact.display_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    weighted_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Opportunity
        fields = [
            'id', 'name', 'contact_name', 'stage', 'estimated_value',
            'probability', 'weighted_value', 'assigned_to_name',
            'expected_close_date', 'created_at'
        ]


class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model."""
    
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_active = serializers.ReadOnlyField()
    roi = serializers.ReadOnlyField()
    
    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'description', 'campaign_type', 'status',
            'start_date', 'end_date', 'budget', 'actual_cost',
            'assigned_to', 'tags', 'assigned_to_name', 'created_by_name',
            'is_active', 'roi', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_active', 'roi', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class SalesStageSerializer(serializers.ModelSerializer):
    """Serializer for SalesStage model."""
    
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = SalesStage
        fields = [
            'id', 'name', 'description', 'probability', 'order',
            'is_closed', 'is_won', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EmailTemplateSerializer(serializers.ModelSerializer):
    """Serializer for EmailTemplate model."""
    
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'name', 'template_type', 'subject', 'body', 'is_active',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class LeadConversionSerializer(serializers.Serializer):
    """Serializer for lead conversion."""
    
    create_contact = serializers.BooleanField(default=True)
    create_opportunity = serializers.BooleanField(default=True)
    opportunity_name = serializers.CharField(max_length=255, required=False)
    opportunity_stage = serializers.CharField(max_length=20, required=False)
    opportunity_estimated_value = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    opportunity_expected_close_date = serializers.DateField(required=False)


class OpportunityStageUpdateSerializer(serializers.Serializer):
    """Serializer for updating opportunity stage."""
    
    stage = serializers.CharField(max_length=20)
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)


class CRMStatsSerializer(serializers.Serializer):
    """Serializer for CRM statistics."""
    
    total_contacts = serializers.IntegerField()
    total_leads = serializers.IntegerField()
    total_opportunities = serializers.IntegerField()
    total_campaigns = serializers.IntegerField()
    
    leads_by_status = serializers.DictField()
    opportunities_by_stage = serializers.DictField()
    
    total_pipeline_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    weighted_pipeline_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    won_opportunities_count = serializers.IntegerField()
    won_opportunities_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    conversion_rate = serializers.FloatField()
    average_deal_size = serializers.DecimalField(max_digits=15, decimal_places=2)


class SalesPipelineSerializer(serializers.Serializer):
    """Serializer for sales pipeline data."""
    
    stage = serializers.CharField()
    count = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    weighted_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    opportunities = OpportunityListSerializer(many=True)
