"""
Serializers for Inventory module.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Category, Brand, Supplier, Product, Warehouse, StockLevel,
    StockMovement, StockAdjustment, StockAdjustmentLine,
    PurchaseOrder, PurchaseOrderLine
)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    full_path = serializers.ReadOnlyField()
    subcategories_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'parent_category', 'is_active',
            'full_path', 'subcategories_count', 'products_count',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'full_path', 'created_at', 'updated_at']
    
    def get_subcategories_count(self, obj):
        return obj.subcategories.filter(is_active=True).count()
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""
    
    products_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'description', 'logo', 'website', 'is_active',
            'products_count', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""
    
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    purchase_orders_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'supplier_type', 'contact_person', 'email', 'phone',
            'website', 'street_address', 'city', 'state', 'postal_code',
            'country', 'tax_id', 'payment_terms', 'credit_limit', 'is_active',
            'rating', 'tags', 'purchase_orders_count', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_purchase_orders_count(self, obj):
        return obj.purchase_orders.count()
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    current_stock = serializers.ReadOnlyField()
    available_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    profit_margin = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'product_type', 'sku', 'barcode',
            'category', 'category_name', 'brand', 'brand_name', 'cost_price',
            'selling_price', 'weight', 'dimensions', 'unit_of_measure',
            'track_inventory', 'minimum_stock_level', 'maximum_stock_level',
            'reorder_point', 'reorder_quantity', 'is_active', 'is_sellable',
            'is_purchasable', 'image', 'tags', 'current_stock', 'available_stock',
            'is_low_stock', 'profit_margin', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'current_stock', 'available_stock', 'is_low_stock',
            'profit_margin', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for Product list views."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    current_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category_name', 'brand_name',
            'cost_price', 'selling_price', 'current_stock', 'is_low_stock',
            'is_active', 'created_at'
        ]


class WarehouseSerializer(serializers.ModelSerializer):
    """Serializer for Warehouse model."""
    
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_products = serializers.SerializerMethodField()
    total_stock_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = [
            'id', 'name', 'code', 'description', 'street_address', 'city',
            'state', 'postal_code', 'country', 'manager', 'manager_name',
            'phone', 'email', 'is_active', 'is_default', 'total_products',
            'total_stock_value', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_products(self, obj):
        return obj.stock_levels.filter(quantity_on_hand__gt=0).count()
    
    def get_total_stock_value(self, obj):
        total = 0
        for stock in obj.stock_levels.filter(quantity_on_hand__gt=0):
            total += stock.quantity_on_hand * stock.product.cost_price
        return total
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StockLevelSerializer(serializers.ModelSerializer):
    """Serializer for StockLevel model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_quantity = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockLevel
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'warehouse',
            'warehouse_name', 'quantity_on_hand', 'quantity_reserved',
            'quantity_on_order', 'available_quantity', 'location',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'available_quantity', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StockMovementSerializer(serializers.ModelSerializer):
    """Serializer for StockMovement model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'warehouse',
            'warehouse_name', 'movement_type', 'quantity', 'unit_cost',
            'reference_type', 'reference_id', 'reference_document',
            'reason', 'notes', 'stock_after_movement', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class StockAdjustmentLineSerializer(serializers.ModelSerializer):
    """Serializer for StockAdjustmentLine model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    
    class Meta:
        model = StockAdjustmentLine
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'expected_quantity',
            'actual_quantity', 'difference', 'unit_cost', 'notes'
        ]
        read_only_fields = ['id', 'difference']


class StockAdjustmentSerializer(serializers.ModelSerializer):
    """Serializer for StockAdjustment model."""
    
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    lines = StockAdjustmentLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = [
            'id', 'adjustment_number', 'adjustment_date', 'adjustment_type',
            'reason', 'warehouse', 'warehouse_name', 'notes', 'total_items',
            'approved_by', 'approved_by_name', 'approved_at', 'lines',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'adjustment_number', 'approved_at', 'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrderLine model."""
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    quantity_pending = serializers.ReadOnlyField()
    is_fully_received = serializers.ReadOnlyField()
    
    class Meta:
        model = PurchaseOrderLine
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'quantity_ordered',
            'quantity_received', 'quantity_pending', 'unit_price', 'line_total',
            'is_fully_received', 'notes'
        ]
        read_only_fields = ['id', 'line_total', 'quantity_pending', 'is_fully_received']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseOrder model."""
    
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    lines = PurchaseOrderLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'supplier', 'supplier_name', 'warehouse',
            'warehouse_name', 'order_date', 'expected_delivery_date',
            'actual_delivery_date', 'status', 'subtotal', 'tax_amount',
            'total_amount', 'notes', 'terms_and_conditions', 'lines',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'po_number', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['organization'] = self.context['request'].user.organization
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    """Simplified serializer for PurchaseOrder list views."""
    
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'supplier_name', 'warehouse_name',
            'order_date', 'expected_delivery_date', 'status',
            'total_amount', 'created_at'
        ]


class InventoryStatsSerializer(serializers.Serializer):
    """Serializer for inventory statistics."""
    
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_brands = serializers.IntegerField()
    total_suppliers = serializers.IntegerField()
    total_warehouses = serializers.IntegerField()
    
    total_stock_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    low_stock_products = serializers.IntegerField()
    out_of_stock_products = serializers.IntegerField()
    
    pending_purchase_orders = serializers.IntegerField()
    pending_adjustments = serializers.IntegerField()
    
    top_products_by_stock = serializers.ListField()
    low_stock_alerts = serializers.ListField()


class StockMovementCreateSerializer(serializers.Serializer):
    """Serializer for creating stock movements."""
    
    product = serializers.UUIDField()
    warehouse = serializers.UUIDField()
    movement_type = serializers.ChoiceField(choices=StockMovement.MOVEMENT_TYPES)
    quantity = serializers.IntegerField()
    unit_cost = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    reference_type = serializers.ChoiceField(choices=StockMovement.REFERENCE_TYPES)
    reference_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    reference_document = serializers.CharField(max_length=255, required=False, allow_blank=True)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class BulkStockUpdateSerializer(serializers.Serializer):
    """Serializer for bulk stock updates."""
    
    updates = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    warehouse = serializers.UUIDField()
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
