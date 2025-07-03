"""
Django admin configuration for Inventory module.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import (
    Category, Brand, Supplier, Product, Warehouse, StockLevel,
    StockMovement, StockAdjustment, StockAdjustmentLine,
    PurchaseOrder, PurchaseOrderLine
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = ['name', 'parent_category', 'full_path', 'is_active', 'products_count', 'created_at']
    list_filter = ['is_active', 'parent_category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'full_path', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'parent_category', 'is_active')
        }),
        ('System Information', {
            'fields': ('id', 'full_path', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def products_count(self, obj):
        return obj.products.filter(is_active=True).count()
    products_count.short_description = 'Products'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent_category')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for Brand model."""
    
    list_display = ['name', 'website', 'is_active', 'products_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'logo', 'website', 'is_active')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def products_count(self, obj):
        return obj.products.filter(is_active=True).count()
    products_count.short_description = 'Products'


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin configuration for Supplier model."""
    
    list_display = ['name', 'supplier_type', 'contact_person', 'email', 'phone', 'rating', 'is_active']
    list_filter = ['supplier_type', 'is_active', 'rating', 'country', 'created_at']
    search_fields = ['name', 'contact_person', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'supplier_type', 'contact_person', 'email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Business Details', {
            'fields': ('tax_id', 'payment_terms', 'credit_limit', 'rating', 'is_active')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    
    list_display = [
        'name', 'sku', 'product_type', 'category', 'brand', 'cost_price',
        'selling_price', 'current_stock_display', 'is_low_stock', 'is_active'
    ]
    list_filter = [
        'product_type', 'category', 'brand', 'is_active', 'is_sellable',
        'is_purchasable', 'track_inventory', 'created_at'
    ]
    search_fields = ['name', 'sku', 'barcode', 'description']
    readonly_fields = [
        'id', 'current_stock', 'available_stock', 'is_low_stock',
        'profit_margin', 'created_at', 'updated_at'
    ]
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'product_type', 'sku', 'barcode', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'brand', 'tags')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price', 'profit_margin')
        }),
        ('Physical Properties', {
            'fields': ('weight', 'dimensions', 'unit_of_measure')
        }),
        ('Inventory Settings', {
            'fields': (
                'track_inventory', 'minimum_stock_level', 'maximum_stock_level',
                'reorder_point', 'reorder_quantity'
            )
        }),
        ('Stock Information', {
            'fields': ('current_stock', 'available_stock', 'is_low_stock'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_sellable', 'is_purchasable')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def current_stock_display(self, obj):
        stock = obj.current_stock
        if obj.is_low_stock:
            return format_html('<span style="color: red;">{}</span>', stock)
        return stock
    current_stock_display.short_description = 'Current Stock'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'brand')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Admin configuration for Warehouse model."""
    
    list_display = ['name', 'code', 'city', 'country', 'manager', 'is_active', 'is_default']
    list_filter = ['is_active', 'is_default', 'country', 'created_at']
    search_fields = ['name', 'code', 'city', 'country']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'manager')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone', 'email')
        }),
        ('Status', {
            'fields': ('is_active', 'is_default')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('manager')


@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    """Admin configuration for StockLevel model."""
    
    list_display = [
        'product', 'warehouse', 'quantity_on_hand', 'quantity_reserved',
        'quantity_on_order', 'available_quantity_display', 'location'
    ]
    list_filter = ['warehouse', 'product__category', 'created_at']
    search_fields = ['product__name', 'product__sku', 'warehouse__name', 'location']
    readonly_fields = ['id', 'available_quantity', 'created_at', 'updated_at']
    ordering = ['product__name']
    
    fieldsets = (
        ('Product & Location', {
            'fields': ('product', 'warehouse', 'location')
        }),
        ('Stock Quantities', {
            'fields': ('quantity_on_hand', 'quantity_reserved', 'quantity_on_order', 'available_quantity')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def available_quantity_display(self, obj):
        return obj.available_quantity
    available_quantity_display.short_description = 'Available'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'warehouse')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """Admin configuration for StockMovement model."""
    
    list_display = [
        'product', 'warehouse', 'movement_type', 'quantity', 'unit_cost',
        'reference_document', 'stock_after_movement', 'created_at'
    ]
    list_filter = ['movement_type', 'reference_type', 'warehouse', 'created_at']
    search_fields = ['product__name', 'product__sku', 'reference_document', 'reason']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Movement Details', {
            'fields': ('product', 'warehouse', 'movement_type', 'quantity', 'unit_cost')
        }),
        ('Reference', {
            'fields': ('reference_type', 'reference_id', 'reference_document')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes', 'stock_after_movement')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'warehouse')


class StockAdjustmentLineInline(admin.TabularInline):
    """Inline for StockAdjustmentLine."""
    
    model = StockAdjustmentLine
    extra = 0
    readonly_fields = ['difference']
    
    fieldsets = (
        (None, {
            'fields': ('product', 'expected_quantity', 'actual_quantity', 'difference', 'unit_cost', 'notes')
        }),
    )


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    """Admin configuration for StockAdjustment model."""
    
    list_display = [
        'adjustment_number', 'adjustment_date', 'adjustment_type', 'warehouse',
        'total_items', 'approval_status', 'created_at'
    ]
    list_filter = ['adjustment_type', 'reason', 'warehouse', 'adjustment_date', 'created_at']
    search_fields = ['adjustment_number', 'notes']
    readonly_fields = ['id', 'adjustment_number', 'approved_at', 'created_at', 'updated_at']
    ordering = ['-adjustment_date']
    inlines = [StockAdjustmentLineInline]
    
    fieldsets = (
        ('Adjustment Details', {
            'fields': ('adjustment_number', 'adjustment_date', 'adjustment_type', 'reason', 'warehouse')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at')
        }),
        ('Additional Information', {
            'fields': ('notes', 'total_items')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def approval_status(self, obj):
        if obj.approved_by:
            return format_html(
                '<span style="color: green;">Approved by {}</span>',
                obj.approved_by.get_full_name()
            )
        return format_html('<span style="color: orange;">Pending Approval</span>')
    approval_status.short_description = 'Status'
    
    actions = ['approve_adjustments']
    
    def approve_adjustments(self, request, queryset):
        """Admin action to approve stock adjustments."""
        count = 0
        for adjustment in queryset.filter(approved_by__isnull=True):
            adjustment.approved_by = request.user
            adjustment.approved_at = timezone.now()
            adjustment.save()
            count += 1
        
        self.message_user(request, f'{count} stock adjustments approved.')
    approve_adjustments.short_description = 'Approve selected stock adjustments'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('warehouse', 'approved_by')


class PurchaseOrderLineInline(admin.TabularInline):
    """Inline for PurchaseOrderLine."""
    
    model = PurchaseOrderLine
    extra = 0
    readonly_fields = ['line_total', 'quantity_pending', 'is_fully_received']
    
    fieldsets = (
        (None, {
            'fields': (
                'product', 'quantity_ordered', 'quantity_received', 'quantity_pending',
                'unit_price', 'line_total', 'is_fully_received', 'notes'
            )
        }),
    )


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    """Admin configuration for PurchaseOrder model."""
    
    list_display = [
        'po_number', 'supplier', 'warehouse', 'order_date',
        'expected_delivery_date', 'status', 'total_amount', 'created_at'
    ]
    list_filter = ['status', 'supplier', 'warehouse', 'order_date', 'created_at']
    search_fields = ['po_number', 'supplier__name', 'notes']
    readonly_fields = ['id', 'po_number', 'created_at', 'updated_at']
    ordering = ['-order_date']
    inlines = [PurchaseOrderLineInline]
    
    fieldsets = (
        ('Order Details', {
            'fields': ('po_number', 'supplier', 'warehouse', 'order_date', 'expected_delivery_date', 'actual_delivery_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Financial', {
            'fields': ('subtotal', 'tax_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_and_conditions')
        }),
        ('System Information', {
            'fields': ('id', 'organization', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_sent', 'mark_as_confirmed']
    
    def mark_as_sent(self, request, queryset):
        """Admin action to mark purchase orders as sent."""
        count = queryset.filter(status='draft').update(status='sent')
        self.message_user(request, f'{count} purchase orders marked as sent.')
    mark_as_sent.short_description = 'Mark selected orders as sent'
    
    def mark_as_confirmed(self, request, queryset):
        """Admin action to mark purchase orders as confirmed."""
        count = queryset.filter(status='sent').update(status='confirmed')
        self.message_user(request, f'{count} purchase orders marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected orders as confirmed'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('supplier', 'warehouse')


# Register the StockAdjustmentLine separately for direct access
@admin.register(StockAdjustmentLine)
class StockAdjustmentLineAdmin(admin.ModelAdmin):
    """Admin configuration for StockAdjustmentLine model."""
    
    list_display = ['adjustment', 'product', 'expected_quantity', 'actual_quantity', 'difference', 'unit_cost']
    list_filter = ['adjustment__adjustment_type', 'adjustment__warehouse']
    search_fields = ['product__name', 'product__sku', 'adjustment__adjustment_number']
    readonly_fields = ['difference']
    ordering = ['adjustment__adjustment_date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('adjustment', 'product')


# Register the PurchaseOrderLine separately for direct access
@admin.register(PurchaseOrderLine)
class PurchaseOrderLineAdmin(admin.ModelAdmin):
    """Admin configuration for PurchaseOrderLine model."""
    
    list_display = [
        'purchase_order', 'product', 'quantity_ordered', 'quantity_received',
        'quantity_pending', 'unit_price', 'line_total', 'is_fully_received'
    ]
    list_filter = ['purchase_order__status', 'purchase_order__supplier', 'is_fully_received']
    search_fields = ['product__name', 'product__sku', 'purchase_order__po_number']
    readonly_fields = ['line_total', 'quantity_pending', 'is_fully_received']
    ordering = ['purchase_order__order_date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('purchase_order', 'product')
