"""
Views for Inventory module.
"""
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, F
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import (
    Category, Brand, Supplier, Product, Warehouse, StockLevel,
    StockMovement, StockAdjustment, StockAdjustmentLine,
    PurchaseOrder, PurchaseOrderLine
)
from .serializers import (
    CategorySerializer, BrandSerializer, SupplierSerializer,
    ProductSerializer, ProductListSerializer, WarehouseSerializer,
    StockLevelSerializer, StockMovementSerializer, StockAdjustmentSerializer,
    PurchaseOrderSerializer, PurchaseOrderListSerializer,
    InventoryStatsSerializer, StockMovementCreateSerializer,
    BulkStockUpdateSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    """List and create categories."""
    
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent_category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Category.objects.filter(organization=self.request.user.organization)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete category."""
    
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(organization=self.request.user.organization)


class BrandListCreateView(generics.ListCreateAPIView):
    """List and create brands."""
    
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Brand.objects.filter(organization=self.request.user.organization)


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete brand."""
    
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Brand.objects.filter(organization=self.request.user.organization)


class SupplierListCreateView(generics.ListCreateAPIView):
    """List and create suppliers."""
    
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier_type', 'is_active', 'rating']
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'rating', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Supplier.objects.filter(organization=self.request.user.organization)


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete supplier."""
    
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Supplier.objects.filter(organization=self.request.user.organization)


class ProductListCreateView(generics.ListCreateAPIView):
    """List and create products."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product_type', 'category', 'brand', 'is_active', 'is_sellable', 'is_purchasable']
    search_fields = ['name', 'description', 'sku', 'barcode']
    ordering_fields = ['name', 'sku', 'cost_price', 'selling_price', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization).select_related('category', 'brand')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete product."""
    
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization).select_related('category', 'brand')


class WarehouseListCreateView(generics.ListCreateAPIView):
    """List and create warehouses."""
    
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_default', 'manager']
    search_fields = ['name', 'code', 'city', 'country']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Warehouse.objects.filter(organization=self.request.user.organization).select_related('manager')


class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete warehouse."""
    
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Warehouse.objects.filter(organization=self.request.user.organization).select_related('manager')


class StockLevelListCreateView(generics.ListCreateAPIView):
    """List and create stock levels."""
    
    serializer_class = StockLevelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'warehouse']
    search_fields = ['product__name', 'product__sku', 'warehouse__name']
    ordering_fields = ['product__name', 'warehouse__name', 'quantity_on_hand', 'created_at']
    ordering = ['product__name']
    
    def get_queryset(self):
        return StockLevel.objects.filter(
            organization=self.request.user.organization
        ).select_related('product', 'warehouse')


class StockLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete stock level."""
    
    serializer_class = StockLevelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StockLevel.objects.filter(
            organization=self.request.user.organization
        ).select_related('product', 'warehouse')


class StockMovementListView(generics.ListAPIView):
    """List stock movements."""
    
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'warehouse', 'movement_type', 'reference_type']
    search_fields = ['product__name', 'product__sku', 'warehouse__name', 'reference_document']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return StockMovement.objects.filter(
            organization=self.request.user.organization
        ).select_related('product', 'warehouse')


class StockAdjustmentListCreateView(generics.ListCreateAPIView):
    """List and create stock adjustments."""
    
    serializer_class = StockAdjustmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['adjustment_type', 'reason', 'warehouse']
    search_fields = ['adjustment_number', 'notes']
    ordering_fields = ['adjustment_date', 'created_at']
    ordering = ['-adjustment_date']
    
    def get_queryset(self):
        return StockAdjustment.objects.filter(
            organization=self.request.user.organization
        ).select_related('warehouse', 'approved_by').prefetch_related('lines__product')


class StockAdjustmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete stock adjustment."""
    
    serializer_class = StockAdjustmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StockAdjustment.objects.filter(
            organization=self.request.user.organization
        ).select_related('warehouse', 'approved_by').prefetch_related('lines__product')


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    """List and create purchase orders."""
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'supplier', 'warehouse']
    search_fields = ['po_number', 'supplier__name', 'notes']
    ordering_fields = ['order_date', 'expected_delivery_date', 'total_amount', 'created_at']
    ordering = ['-order_date']
    
    def get_queryset(self):
        return PurchaseOrder.objects.filter(
            organization=self.request.user.organization
        ).select_related('supplier', 'warehouse')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PurchaseOrderListSerializer
        return PurchaseOrderSerializer


class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete purchase order."""
    
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PurchaseOrder.objects.filter(
            organization=self.request.user.organization
        ).select_related('supplier', 'warehouse').prefetch_related('lines__product')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stock_movement_view(request):
    """Create a stock movement and update stock levels."""
    
    serializer = StockMovementCreateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Get product and warehouse
        try:
            product = Product.objects.get(
                id=data['product'],
                organization=request.user.organization
            )
            warehouse = Warehouse.objects.get(
                id=data['warehouse'],
                organization=request.user.organization
            )
        except (Product.DoesNotExist, Warehouse.DoesNotExist):
            return Response(
                {'error': 'Product or warehouse not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        with transaction.atomic():
            # Get or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                product=product,
                warehouse=warehouse,
                defaults={
                    'organization': request.user.organization,
                    'created_by': request.user
                }
            )
            
            # Calculate new stock level
            if data['movement_type'] in ['in', 'return']:
                new_quantity = stock_level.quantity_on_hand + data['quantity']
            else:  # out, transfer, adjustment, damaged, expired
                new_quantity = max(0, stock_level.quantity_on_hand - abs(data['quantity']))
            
            # Create stock movement
            movement = StockMovement.objects.create(
                organization=request.user.organization,
                product=product,
                warehouse=warehouse,
                movement_type=data['movement_type'],
                quantity=data['quantity'],
                unit_cost=data.get('unit_cost'),
                reference_type=data['reference_type'],
                reference_id=data.get('reference_id', ''),
                reference_document=data.get('reference_document', ''),
                reason=data.get('reason', ''),
                notes=data.get('notes', ''),
                stock_after_movement=new_quantity,
                created_by=request.user
            )
            
            # Update stock level
            stock_level.quantity_on_hand = new_quantity
            stock_level.updated_by = request.user
            stock_level.save()
        
        return Response({
            'message': 'Stock movement created successfully',
            'movement_id': str(movement.id),
            'new_stock_level': new_quantity
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_stock_update_view(request):
    """Bulk update stock levels."""
    
    serializer = BulkStockUpdateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        
        try:
            warehouse = Warehouse.objects.get(
                id=data['warehouse'],
                organization=request.user.organization
            )
        except Warehouse.DoesNotExist:
            return Response(
                {'error': 'Warehouse not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        updated_count = 0
        errors = []
        
        with transaction.atomic():
            for update in data['updates']:
                try:
                    product = Product.objects.get(
                        id=update['product_id'],
                        organization=request.user.organization
                    )
                    
                    stock_level, created = StockLevel.objects.get_or_create(
                        product=product,
                        warehouse=warehouse,
                        defaults={
                            'organization': request.user.organization,
                            'created_by': request.user
                        }
                    )
                    
                    old_quantity = stock_level.quantity_on_hand
                    new_quantity = int(update['new_quantity'])
                    difference = new_quantity - old_quantity
                    
                    if difference != 0:
                        # Create stock movement
                        StockMovement.objects.create(
                            organization=request.user.organization,
                            product=product,
                            warehouse=warehouse,
                            movement_type='adjustment',
                            quantity=difference,
                            reference_type='adjustment',
                            reason=data.get('reason', 'Bulk update'),
                            notes=data.get('notes', ''),
                            stock_after_movement=new_quantity,
                            created_by=request.user
                        )
                        
                        # Update stock level
                        stock_level.quantity_on_hand = new_quantity
                        stock_level.updated_by = request.user
                        stock_level.save()
                        
                        updated_count += 1
                
                except (Product.DoesNotExist, ValueError) as e:
                    errors.append(f"Error updating product {update.get('product_id', 'unknown')}: {str(e)}")
        
        return Response({
            'message': f'Bulk update completed. {updated_count} products updated.',
            'updated_count': updated_count,
            'errors': errors
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_stats_view(request):
    """Get inventory statistics."""
    
    organization = request.user.organization
    
    # Basic counts
    total_products = Product.objects.filter(organization=organization, is_active=True).count()
    total_categories = Category.objects.filter(organization=organization, is_active=True).count()
    total_brands = Brand.objects.filter(organization=organization, is_active=True).count()
    total_suppliers = Supplier.objects.filter(organization=organization, is_active=True).count()
    total_warehouses = Warehouse.objects.filter(organization=organization, is_active=True).count()
    
    # Stock value calculation
    total_stock_value = 0
    low_stock_count = 0
    out_of_stock_count = 0
    
    for product in Product.objects.filter(organization=organization, is_active=True, track_inventory=True):
        current_stock = product.current_stock
        if current_stock == 0:
            out_of_stock_count += 1
        elif current_stock <= product.minimum_stock_level:
            low_stock_count += 1
        
        total_stock_value += current_stock * product.cost_price
    
    # Purchase orders
    pending_purchase_orders = PurchaseOrder.objects.filter(
        organization=organization,
        status__in=['draft', 'sent', 'confirmed', 'partially_received']
    ).count()
    
    # Stock adjustments
    pending_adjustments = StockAdjustment.objects.filter(
        organization=organization,
        approved_by__isnull=True
    ).count()
    
    # Top products by stock value
    top_products = []
    for product in Product.objects.filter(organization=organization, is_active=True)[:10]:
        stock_value = product.current_stock * product.cost_price
        if stock_value > 0:
            top_products.append({
                'id': str(product.id),
                'name': product.name,
                'sku': product.sku,
                'current_stock': product.current_stock,
                'stock_value': float(stock_value)
            })
    
    top_products.sort(key=lambda x: x['stock_value'], reverse=True)
    top_products = top_products[:5]
    
    # Low stock alerts
    low_stock_alerts = []
    for product in Product.objects.filter(organization=organization, is_active=True, track_inventory=True):
        if product.is_low_stock:
            low_stock_alerts.append({
                'id': str(product.id),
                'name': product.name,
                'sku': product.sku,
                'current_stock': product.current_stock,
                'minimum_stock_level': product.minimum_stock_level
            })
    
    stats = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_brands': total_brands,
        'total_suppliers': total_suppliers,
        'total_warehouses': total_warehouses,
        'total_stock_value': total_stock_value,
        'low_stock_products': low_stock_count,
        'out_of_stock_products': out_of_stock_count,
        'pending_purchase_orders': pending_purchase_orders,
        'pending_adjustments': pending_adjustments,
        'top_products_by_stock': top_products,
        'low_stock_alerts': low_stock_alerts
    }
    
    serializer = InventoryStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def low_stock_products_view(request):
    """Get products with low stock levels."""
    
    products = Product.objects.filter(
        organization=request.user.organization,
        is_active=True,
        track_inventory=True
    )
    
    low_stock_products = []
    for product in products:
        if product.is_low_stock:
            low_stock_products.append(product)
    
    serializer = ProductListSerializer(low_stock_products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_stock_history_view(request, pk):
    """Get stock movement history for a product."""
    
    try:
        product = Product.objects.get(
            pk=pk,
            organization=request.user.organization
        )
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    movements = StockMovement.objects.filter(
        product=product,
        organization=request.user.organization
    ).select_related('warehouse').order_by('-created_at')
    
    serializer = StockMovementSerializer(movements, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_stock_adjustment_view(request, pk):
    """Approve a stock adjustment."""
    
    try:
        adjustment = StockAdjustment.objects.get(
            pk=pk,
            organization=request.user.organization
        )
    except StockAdjustment.DoesNotExist:
        return Response(
            {'error': 'Stock adjustment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if adjustment.approved_by:
        return Response(
            {'error': 'Stock adjustment already approved'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    with transaction.atomic():
        # Approve the adjustment
        adjustment.approved_by = request.user
        adjustment.approved_at = timezone.now()
        adjustment.save()
        
        # Process adjustment lines
        for line in adjustment.lines.all():
            if line.difference != 0:
                # Get or create stock level
                stock_level, created = StockLevel.objects.get_or_create(
                    product=line.product,
                    warehouse=adjustment.warehouse,
                    defaults={
                        'organization': request.user.organization,
                        'created_by': request.user
                    }
                )
                
                # Create stock movement
                StockMovement.objects.create(
                    organization=request.user.organization,
                    product=line.product,
                    warehouse=adjustment.warehouse,
                    movement_type='adjustment',
                    quantity=line.difference,
                    unit_cost=line.unit_cost,
                    reference_type='adjustment',
                    reference_id=adjustment.adjustment_number,
                    reason=adjustment.reason,
                    notes=f"Stock adjustment: {adjustment.adjustment_number}",
                    stock_after_movement=line.actual_quantity,
                    created_by=request.user
                )
                
                # Update stock level
                stock_level.quantity_on_hand = line.actual_quantity
                stock_level.updated_by = request.user
                stock_level.save()
    
    return Response({
        'message': 'Stock adjustment approved successfully'
    }, status=status.HTTP_200_OK)
