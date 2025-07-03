"""
Admin configuration for CRM module.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Contact, Lead, Opportunity, Campaign, SalesStage, EmailTemplate


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin for Contact model."""
    
    list_display = [
        'display_name', 'contact_type', 'email', 'phone', 'city', 
        'country', 'is_active', 'created_at'
    ]
    list_filter = [
        'contact_type', 'is_active', 'industry', 'country', 
        'organization', 'created_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'company_name', 'email', 
        'phone', 'mobile'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at', 'full_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'contact_type', 'salutation', 'first_name', 'last_name',
                'company_name', 'job_title'
            )
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'mobile', 'website')
        }),
        ('Address', {
            'fields': (
                'street_address', 'city', 'state', 'postal_code', 'country'
            ),
            'classes': ('collapse',)
        }),
        ('Business Information', {
            'fields': ('industry', 'annual_revenue', 'employee_count'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_handle', 'facebook_url'),
            'classes': ('collapse',)
        }),
        ('Relationship & Status', {
            'fields': ('parent_contact', 'is_active', 'tags', 'source', 'description')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def display_name(self, obj):
        return obj.display_name
    display_name.short_description = 'Name'


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin for Lead model."""
    
    list_display = [
        'title', 'contact_name', 'company_name', 'status', 'priority',
        'estimated_value', 'assigned_to', 'expected_close_date', 'is_converted'
    ]
    list_filter = [
        'status', 'priority', 'source', 'assigned_to', 
        'organization', 'created_at'
    ]
    search_fields = ['title', 'contact_name', 'company_name', 'email']
    readonly_fields = [
        'id', 'is_converted', 'converted_contact', 'converted_opportunity',
        'converted_at', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'expected_close_date'
    
    fieldsets = (
        ('Lead Information', {
            'fields': ('title', 'description', 'status', 'priority', 'source')
        }),
        ('Contact Details', {
            'fields': ('contact_name', 'company_name', 'email', 'phone')
        }),
        ('Sales Information', {
            'fields': (
                'estimated_value', 'probability', 'assigned_to', 
                'expected_close_date'
            )
        }),
        ('Conversion', {
            'fields': (
                'is_converted', 'converted_contact', 'converted_opportunity',
                'converted_at'
            ),
            'classes': ('collapse',)
        }),
        ('Tags & Metadata', {
            'fields': ('tags', 'id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def is_converted(self, obj):
        return obj.is_converted
    is_converted.boolean = True
    is_converted.short_description = 'Converted'


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    """Admin for Opportunity model."""
    
    list_display = [
        'name', 'contact', 'stage', 'estimated_value', 'probability',
        'weighted_value', 'assigned_to', 'expected_close_date', 'is_closed'
    ]
    list_filter = [
        'stage', 'priority', 'assigned_to', 'organization', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'contact__first_name', 
        'contact__last_name', 'contact__company_name'
    ]
    readonly_fields = [
        'id', 'is_closed', 'is_won', 'weighted_value', 
        'actual_close_date', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'expected_close_date'
    
    fieldsets = (
        ('Opportunity Information', {
            'fields': ('name', 'description', 'contact', 'stage', 'priority')
        }),
        ('Financial Details', {
            'fields': ('estimated_value', 'probability', 'weighted_value')
        }),
        ('Assignment & Dates', {
            'fields': (
                'assigned_to', 'expected_close_date', 'actual_close_date'
            )
        }),
        ('Additional Information', {
            'fields': ('competitors', 'lead_source', 'tags'),
            'classes': ('collapse',)
        }),
        ('Status & Metadata', {
            'fields': ('is_closed', 'is_won', 'id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def weighted_value(self, obj):
        return f"${obj.weighted_value:,.2f}"
    weighted_value.short_description = 'Weighted Value'
    
    def is_closed(self, obj):
        return obj.is_closed
    is_closed.boolean = True
    is_closed.short_description = 'Closed'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin for Campaign model."""
    
    list_display = [
        'name', 'campaign_type', 'status', 'start_date', 'end_date',
        'budget', 'actual_cost', 'roi_display', 'assigned_to'
    ]
    list_filter = [
        'campaign_type', 'status', 'assigned_to', 'organization', 'start_date'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'is_active', 'roi', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('name', 'description', 'campaign_type', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'assigned_to')
        }),
        ('Budget & Performance', {
            'fields': ('budget', 'actual_cost', 'roi')
        }),
        ('Tags & Metadata', {
            'fields': ('tags', 'is_active', 'id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def roi_display(self, obj):
        roi = obj.roi
        if roi > 0:
            return format_html(
                '<span style="color: green;">+{:.1f}%</span>', roi
            )
        elif roi < 0:
            return format_html(
                '<span style="color: red;">{:.1f}%</span>', roi
            )
        return f"{roi:.1f}%"
    roi_display.short_description = 'ROI'


@admin.register(SalesStage)
class SalesStageAdmin(admin.ModelAdmin):
    """Admin for SalesStage model."""
    
    list_display = [
        'name', 'probability', 'order', 'is_closed', 'is_won', 'organization'
    ]
    list_filter = ['is_closed', 'is_won', 'organization']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['order']
    
    fieldsets = (
        ('Stage Information', {
            'fields': ('name', 'description', 'probability', 'order')
        }),
        ('Status', {
            'fields': ('is_closed', 'is_won')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """Admin for EmailTemplate model."""
    
    list_display = [
        'name', 'template_type', 'subject_preview', 'is_active', 'created_at'
    ]
    list_filter = ['template_type', 'is_active', 'organization', 'created_at']
    search_fields = ['name', 'subject', 'body']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_type', 'is_active')
        }),
        ('Email Content', {
            'fields': ('subject', 'body')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def subject_preview(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    subject_preview.short_description = 'Subject'


# Custom admin actions
@admin.action(description='Mark selected leads as contacted')
def mark_leads_contacted(modeladmin, request, queryset):
    queryset.update(status='contacted')


@admin.action(description='Mark selected opportunities as won')
def mark_opportunities_won(modeladmin, request, queryset):
    for opportunity in queryset:
        opportunity.close_as_won(request.user)


@admin.action(description='Mark selected opportunities as lost')
def mark_opportunities_lost(modeladmin, request, queryset):
    for opportunity in queryset:
        opportunity.close_as_lost(request.user)


# Add actions to admin classes
LeadAdmin.actions = [mark_leads_contacted]
OpportunityAdmin.actions = [mark_opportunities_won, mark_opportunities_lost]
