"""
CRM models for customer relationship management.
"""
from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from apps.core.models import BaseModel
import uuid


class Contact(BaseModel):
    """Contact model for customers and prospects."""
    
    CONTACT_TYPES = [
        ('person', 'Person'),
        ('company', 'Company'),
    ]
    
    SALUTATION_CHOICES = [
        ('mr', 'Mr.'),
        ('mrs', 'Mrs.'),
        ('ms', 'Ms.'),
        ('dr', 'Dr.'),
        ('prof', 'Prof.'),
    ]
    
    # Basic Information
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='person')
    salutation = models.CharField(max_length=10, choices=SALUTATION_CHOICES, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    mobile = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    website = models.URLField(blank=True)
    
    # Address Information
    street_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Business Information
    industry = models.CharField(max_length=100, blank=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Relationship
    parent_contact = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='child_contacts'
    )
    
    # Social Media
    linkedin_url = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    facebook_url = models.URLField(blank=True)
    
    # Status and Tags
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    # Metadata
    source = models.CharField(max_length=100, blank=True)  # How we got this contact
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'crm_contacts'
        ordering = ['first_name', 'last_name', 'company_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['organization', 'is_active']),
            models.Index(fields=['contact_type']),
        ]
    
    def __str__(self):
        if self.contact_type == 'company':
            return self.company_name or f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        if self.contact_type == 'company':
            return self.company_name
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self):
        if self.contact_type == 'company':
            return self.company_name
        name = f"{self.first_name} {self.last_name}".strip()
        if self.company_name:
            name += f" ({self.company_name})"
        return name


class Lead(BaseModel):
    """Lead model for potential customers."""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('email_campaign', 'Email Campaign'),
        ('cold_call', 'Cold Call'),
        ('trade_show', 'Trade Show'),
        ('advertisement', 'Advertisement'),
        ('partner', 'Partner'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Contact Information (before converting to Contact)
    contact_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Lead Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='website')
    
    # Financial Information
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    probability = models.PositiveIntegerField(default=0, help_text="Probability of closing (0-100%)")
    
    # Assignment and Dates
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    expected_close_date = models.DateField(null=True, blank=True)
    
    # Conversion
    converted_contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='converted_from_leads'
    )
    converted_opportunity = models.ForeignKey(
        'Opportunity',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='converted_from_leads'
    )
    converted_at = models.DateTimeField(null=True, blank=True)
    
    # Tags and Notes
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    class Meta:
        db_table = 'crm_leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'assigned_to']),
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['expected_close_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.contact_name}"
    
    @property
    def is_converted(self):
        return self.converted_contact is not None or self.converted_opportunity is not None
    
    def convert_to_contact_and_opportunity(self, user):
        """Convert lead to contact and opportunity."""
        if self.is_converted:
            return self.converted_contact, self.converted_opportunity
        
        # Create contact
        contact = Contact.objects.create(
            organization=self.organization,
            first_name=self.contact_name.split()[0] if self.contact_name else '',
            last_name=' '.join(self.contact_name.split()[1:]) if len(self.contact_name.split()) > 1 else '',
            company_name=self.company_name,
            email=self.email,
            phone=self.phone,
            source=self.source,
            created_by=user
        )
        
        # Create opportunity
        opportunity = Opportunity.objects.create(
            organization=self.organization,
            name=self.title,
            contact=contact,
            description=self.description,
            stage='qualification',
            estimated_value=self.estimated_value,
            probability=self.probability,
            expected_close_date=self.expected_close_date,
            assigned_to=self.assigned_to,
            created_by=user
        )
        
        # Update lead
        self.converted_contact = contact
        self.converted_opportunity = opportunity
        self.converted_at = timezone.now()
        self.status = 'qualified'
        self.save()
        
        return contact, opportunity


class Opportunity(BaseModel):
    """Opportunity model for sales opportunities."""
    
    STAGE_CHOICES = [
        ('qualification', 'Qualification'),
        ('needs_analysis', 'Needs Analysis'),
        ('proposal', 'Proposal/Quote'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Relationship
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='opportunities'
    )
    
    # Opportunity Details
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='qualification')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Financial Information
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2)
    probability = models.PositiveIntegerField(default=0, help_text="Probability of closing (0-100%)")
    
    # Assignment and Dates
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_opportunities'
    )
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(null=True, blank=True)
    
    # Competition and Source
    competitors = models.TextField(blank=True, help_text="List of competitors")
    lead_source = models.CharField(max_length=100, blank=True)
    
    # Tags
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    class Meta:
        db_table = 'crm_opportunities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stage', 'assigned_to']),
            models.Index(fields=['organization', 'stage']),
            models.Index(fields=['expected_close_date']),
            models.Index(fields=['contact']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.contact.display_name}"
    
    @property
    def is_closed(self):
        return self.stage in ['closed_won', 'closed_lost']
    
    @property
    def is_won(self):
        return self.stage == 'closed_won'
    
    @property
    def weighted_value(self):
        return (self.estimated_value * self.probability) / 100
    
    def close_as_won(self, user):
        """Close opportunity as won."""
        self.stage = 'closed_won'
        self.actual_close_date = timezone.now().date()
        self.probability = 100
        self.updated_by = user
        self.save()
    
    def close_as_lost(self, user, reason=''):
        """Close opportunity as lost."""
        self.stage = 'closed_lost'
        self.actual_close_date = timezone.now().date()
        self.probability = 0
        self.updated_by = user
        self.save()
        
        # Add note with reason if provided
        if reason:
            from apps.core.models import Note
            from django.contrib.contenttypes.models import ContentType
            
            Note.objects.create(
                organization=self.organization,
                content=f"Opportunity closed as lost. Reason: {reason}",
                content_type=ContentType.objects.get_for_model(self),
                object_id=str(self.id),
                created_by=user
            )


class Campaign(BaseModel):
    """Marketing campaign model."""
    
    CAMPAIGN_TYPES = [
        ('email', 'Email Campaign'),
        ('social_media', 'Social Media'),
        ('advertisement', 'Advertisement'),
        ('event', 'Event'),
        ('webinar', 'Webinar'),
        ('content', 'Content Marketing'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Budget and Metrics
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_campaigns'
    )
    
    # Tags
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    class Meta:
        db_table = 'crm_campaigns'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['organization', 'status']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def is_active(self):
        today = timezone.now().date()
        return (
            self.status == 'active' and 
            self.start_date <= today <= self.end_date
        )
    
    @property
    def roi(self):
        """Calculate return on investment."""
        if not self.actual_cost or self.actual_cost == 0:
            return 0
        
        # Calculate revenue from opportunities created by this campaign
        revenue = sum(
            opp.estimated_value for opp in 
            Opportunity.objects.filter(
                lead_source=self.name,
                stage='closed_won',
                organization=self.organization
            )
        )
        
        return ((revenue - self.actual_cost) / self.actual_cost) * 100


class SalesStage(BaseModel):
    """Custom sales stages for opportunities."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    probability = models.PositiveIntegerField(default=0, help_text="Default probability for this stage (0-100%)")
    order = models.PositiveIntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    is_won = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'crm_sales_stages'
        ordering = ['order']
        unique_together = ['organization', 'name']
    
    def __str__(self):
        return self.name


class EmailTemplate(BaseModel):
    """Email template for CRM communications."""
    
    TEMPLATE_TYPES = [
        ('lead_follow_up', 'Lead Follow Up'),
        ('opportunity_proposal', 'Opportunity Proposal'),
        ('welcome', 'Welcome Email'),
        ('thank_you', 'Thank You'),
        ('newsletter', 'Newsletter'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=255)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'crm_email_templates'
        ordering = ['name']
    
    def __str__(self):
        return self.name
