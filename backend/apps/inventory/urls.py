"""
URL configuration for Inventory module.
"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Brands
    path('brands/', views.BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<uuid:pk>/', views.BrandDetailView.as_view(), name='brand-detail'),
    
    # Suppliers
    path('suppliers/', views.SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<uuid:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    
    # Products
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<uuid:pk>/stock-history/', views.product_stock_history_view, name='product-stock-history'),
    
    # Warehouses
    path('warehouses/', views.WarehouseListCreateView.as_view(), name='warehouse-list-create'),
    path('warehouses/<uuid:pk>/', views.WarehouseDetailView.as_view(), name='warehouse-detail'),
    
    # Stock Levels
    path('stock-levels/', views.StockLevelListCreateView.as_view(), name='stock-level-list-create'),
    path('stock-levels/<uuid:pk>/', views.StockLevelDetailView.as_view(), name='stock-level-detail'),
    
    # Stock Movements
    path('stock-movements/', views.StockMovementListView.as_view(), name='stock-movement-list'),
    path('stock-movements/create/', views.create_stock_movement_view, name='stock-movement-create'),
    path('stock-movements/bulk-update/', views.bulk_stock_update_view, name='bulk-stock-update'),
    
    # Stock Adjustments
    path('stock-adjustments/', views.StockAdjustmentListCreateView.as_view(), name='stock-adjustment-list-create'),
    path('stock-adjustments/<uuid:pk>/', views.StockAdjustmentDetailView.as_view(), name='stock-adjustment-detail'),
    path('stock-adjustments/<uuid:pk>/approve/', views.approve_stock_adjustment_view, name='stock-adjustment-approve'),
    
    # Purchase Orders
    path('purchase-orders/', views.PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase-orders/<uuid:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    
    # Analytics and Reports
    path('stats/', views.inventory_stats_view, name='inventory-stats'),
    path('low-stock/', views.low_stock_products_view, name='low-stock-products'),
]
