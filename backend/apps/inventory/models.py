"""
Inventory management models for products, stock, and warehouses.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from apps.core.models import BaseModel
import uuid


class Category(BaseModel):
    """Product category model."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['organization', 'name', 'parent_category']
    
    def __str__(self):
        if self.parent_category:
            return f"{self.parent_category.name} > {self.name}"
        return self.name
    
    @property
    def full_path(self):
        """Get full category path."""
        path = [self.name]
        parent = self.parent_category
        while parent:
            path.insert(0, parent.name)
            parent = parent.parent_category
        return " > ".join(path)


class Brand(BaseModel):
    """Product brand model."""
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_brands'
        ordering = ['name']
        unique_together = ['organization', 'name']
    
    def __str__(self):
        return self.name


class Supplier(BaseModel):
    """Supplier model for inventory management."""
    
    SUPPLIER_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('wholesaler', 'Wholesaler'),
        ('retailer', 'Retailer'),
        ('service_provider', 'Service Provider'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES)
    contact_person = models.CharField(max_length=255, blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    street_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Business Information
    tax_id = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    rating = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Rating from 1-5"
    )
    
    # Tags
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    class Meta:
        db_table = 'inventory_suppliers'
        ordering = ['name']
        unique_together = ['organization', 'name']
    
    def __str__(self):
        return self.name


class Product(BaseModel):
    """Product model for inventory management."""
    
    PRODUCT_TYPES = [
        ('physical', 'Physical Product'),
        ('digital', 'Digital Product'),
        ('service', 'Service'),
        ('bundle', 'Bundle'),
    ]
    
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('lb', 'Pound'),
        ('oz', 'Ounce'),
        ('liter', 'Liter'),
        ('ml', 'Milliliter'),
        ('gallon', 'Gallon'),
        ('meter', 'Meter'),
        ('cm', 'Centimeter'),
        ('inch', 'Inch'),
        ('foot', 'Foot'),
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='physical')
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True)
    
    # Classification
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Pricing
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Physical Properties
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    dimensions = models.CharField(max_length=100, blank=True, help_text="L x W x H")
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece')
    
    # Inventory Settings
    track_inventory = models.BooleanField(default=True)
    minimum_stock_level = models.PositiveIntegerField(default=0)
    maximum_stock_level = models.PositiveIntegerField(null=True, blank=True)
    reorder_point = models.PositiveIntegerField(default=0)
    reorder_quantity = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_sellable = models.BooleanField(default=True)
    is_purchasable = models.BooleanField(default=True)
    
    # Images
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Tags
    tags = models.ManyToManyField('core.Tag', blank=True)
    
    class Meta:
        db_table = 'inventory_products'
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['organization', 'is_active']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def current_stock(self):
        """Get current stock across all warehouses."""
        return sum(
            stock.quantity_on_hand 
            for stock in self.stock_levels.filter(warehouse__is_active=True)
        )
    
    @property
    def available_stock(self):
        """Get available stock (on hand - reserved)."""
        return sum(
            stock.available_quantity 
            for stock in self.stock_levels.filter(warehouse__is_active=True)
        )
    
    @property
    def is_low_stock(self):
        """Check if product is below minimum stock level."""
        return self.current_stock <= self.minimum_stock_level
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0


class Warehouse(BaseModel):
    """Warehouse model for inventory locations."""
    
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    # Address
    street_address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Contact Information
    manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_warehouses'
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'inventory_warehouses'
        ordering = ['name']
        unique_together = ['organization', 'code']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        # Ensure only one default warehouse per organization
        if self.is_default:
            Warehouse.objects.filter(
                organization=self.organization,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class StockLevel(BaseModel):
    """Stock level tracking for products in warehouses."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_levels'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_levels'
    )
    
    # Stock Quantities
    quantity_on_hand = models.PositiveIntegerField(default=0)
    quantity_reserved = models.PositiveIntegerField(default=0)
    quantity_on_order = models.PositiveIntegerField(default=0)
    
    # Location within warehouse
    location = models.CharField(max_length=100, blank=True, help_text="Aisle, Shelf, Bin, etc.")
    
    class Meta:
        db_table = 'inventory_stock_levels'
        unique_together = ['product', 'warehouse']
        indexes = [
            models.Index(fields=['product', 'warehouse']),
            models.Index(fields=['warehouse']),
        ]
    
    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name}: {self.quantity_on_hand}"
    
    @property
    def available_quantity(self):
        """Get available quantity (on hand - reserved)."""
        return max(0, self.quantity_on_hand - self.quantity_reserved)


class StockMovement(BaseModel):
    """Stock movement tracking for inventory transactions."""
    
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
        ('damaged', 'Damaged'),
        ('expired', 'Expired'),
    ]
    
    REFERENCE_TYPES = [
        ('purchase_order', 'Purchase Order'),
        ('sales_order', 'Sales Order'),
        ('transfer_order', 'Transfer Order'),
        ('adjustment', 'Stock Adjustment'),
        ('return', 'Return'),
        ('manual', 'Manual Entry'),
    ]
    
    # Basic Information
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    
    # Movement Details
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()  # Can be negative for outbound movements
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Reference Information
    reference_type = models.CharField(max_length=20, choices=REFERENCE_TYPES)
    reference_id = models.CharField(max_length=100, blank=True)
    reference_document = models.CharField(max_length=255, blank=True)
    
    # Additional Information
    reason = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    # Stock levels after this movement
    stock_after_movement = models.PositiveIntegerField()
    
    class Meta:
        db_table = 'inventory_stock_movements'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'warehouse']),
            models.Index(fields=['movement_type', 'created_at']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.movement_type}: {self.quantity}"


class StockAdjustment(BaseModel):
    """Stock adjustment for inventory corrections."""
    
    ADJUSTMENT_TYPES = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
        ('recount', 'Physical Recount'),
    ]
    
    REASONS = [
        ('damaged', 'Damaged Goods'),
        ('expired', 'Expired Products'),
        ('theft', 'Theft/Loss'),
        ('found', 'Found Stock'),
        ('recount', 'Physical Count Correction'),
        ('system_error', 'System Error'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    adjustment_number = models.CharField(max_length=50, unique=True)
    adjustment_date = models.DateField(default=timezone.now)
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES)
    reason = models.CharField(max_length=20, choices=REASONS)
    
    # Reference
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='stock_adjustments'
    )
    
    # Details
    notes = models.TextField(blank=True)
    total_items = models.PositiveIntegerField(default=0)
    
    # Approval
    approved_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_adjustments'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_stock_adjustments'
        ordering = ['-adjustment_date']
    
    def __str__(self):
        return f"Adjustment {self.adjustment_number} - {self.warehouse.name}"
    
    def save(self, *args, **kwargs):
        if not self.adjustment_number:
            # Generate adjustment number
            today = timezone.now().date()
            count = StockAdjustment.objects.filter(
                organization=self.organization,
                created_at__date=today
            ).count() + 1
            self.adjustment_number = f"ADJ-{today.strftime('%Y%m%d')}-{count:04d}"
        super().save(*args, **kwargs)


class StockAdjustmentLine(BaseModel):
    """Individual line items for stock adjustments."""
    
    adjustment = models.ForeignKey(
        StockAdjustment,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='adjustment_lines'
    )
    
    # Quantities
    expected_quantity = models.PositiveIntegerField()
    actual_quantity = models.PositiveIntegerField()
    difference = models.IntegerField()  # actual - expected
    
    # Cost
    unit_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_stock_adjustment_lines'
        unique_together = ['adjustment', 'product']
    
    def __str__(self):
        return f"{self.adjustment.adjustment_number} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        self.difference = self.actual_quantity - self.expected_quantity
        super().save(*args, **kwargs)


class PurchaseOrder(BaseModel):
    """Purchase order model for inventory procurement."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('confirmed', 'Confirmed'),
        ('partially_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='purchase_orders'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='purchase_orders'
    )
    
    # Dates
    order_date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    
    # Status and Financial
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Additional Information
    notes = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_purchase_orders'
        ordering = ['-order_date']
    
    def __str__(self):
        return f"PO {self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            # Generate PO number
            today = timezone.now().date()
            count = PurchaseOrder.objects.filter(
                organization=self.organization,
                created_at__date=today
            ).count() + 1
            self.po_number = f"PO-{today.strftime('%Y%m%d')}-{count:04d}"
        super().save(*args, **kwargs)


class PurchaseOrderLine(BaseModel):
    """Purchase order line items."""
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='purchase_order_lines'
    )
    
    # Quantities and Pricing
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    line_total = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_purchase_order_lines'
        unique_together = ['purchase_order', 'product']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.product.name}"
    
    @property
    def quantity_pending(self):
        """Get quantity still pending delivery."""
        return max(0, self.quantity_ordered - self.quantity_received)
    
    @property
    def is_fully_received(self):
        """Check if line is fully received."""
        return self.quantity_received >= self.quantity_ordered
    
    def save(self, *args, **kwargs):
        self.line_total = self.quantity_ordered * self.unit_price
        super().save(*args, **kwargs)
