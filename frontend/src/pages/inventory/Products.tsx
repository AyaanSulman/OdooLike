import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  Tooltip,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { fetchProducts, deleteProduct } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';

const Products: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { products, isLoading } = useSelector((state: RootState) => state.inventory);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage: number) => {
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const handleAddProduct = () => {
    navigate('/inventory/products/new');
  };

  const handleEditProduct = (product: any) => {
    navigate(`/inventory/products/${product.id}`);
  };

  const handleViewProduct = (product: any) => {
    navigate(`/inventory/products/${product.id}/view`);
  };

  const handleDeleteClick = (ids: string[]) => {
    setSelectedIds(ids);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    await Promise.all(selectedIds.map((id) => dispatch(deleteProduct(id))));
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  // Mock data for demonstration
  const mockProducts = [
    {
      id: '1',
      name: 'Laptop XPS 15',
      sku: 'LAP-XPS-15',
      category: 'Electronics',
      price: 1299.99,
      cost: 950.00,
      stock_quantity: 15,
      status: 'Active',
    },
    {
      id: '2',
      name: 'Wireless Mouse',
      sku: 'ACC-MOU-01',
      category: 'Accessories',
      price: 29.99,
      cost: 12.50,
      stock_quantity: 45,
      status: 'Active',
    },
    {
      id: '3',
      name: 'USB-C Cable',
      sku: 'CAB-USBC-01',
      category: 'Cables',
      price: 19.99,
      cost: 5.00,
      stock_quantity: 120,
      status: 'Active',
    },
    {
      id: '4',
      name: 'Monitor 27"',
      sku: 'MON-27-01',
      category: 'Electronics',
      price: 349.99,
      cost: 220.00,
      stock_quantity: 8,
      status: 'Active',
    },
    {
      id: '5',
      name: 'Keyboard Mechanical',
      sku: 'KEY-MECH-01',
      category: 'Accessories',
      price: 89.99,
      cost: 45.00,
      stock_quantity: 25,
      status: 'Active',
    },
  ];

  const productData = products?.length > 0 ? products : mockProducts;

  const columns = [
    { id: 'name', label: 'Product Name', minWidth: 180 },
    { id: 'sku', label: 'SKU', minWidth: 120 },
    { id: 'category', label: 'Category', minWidth: 120 },
    {
      id: 'price',
      label: 'Price',
      minWidth: 100,
      align: 'right' as const,
      format: (value: number) => `$${value.toFixed(2)}`,
    },
    {
      id: 'cost',
      label: 'Cost',
      minWidth: 100,
      align: 'right' as const,
      format: (value: number) => `$${value.toFixed(2)}`,
    },
    {
      id: 'stock_quantity',
      label: 'Stock',
      minWidth: 80,
      align: 'right' as const,
    },
    { id: 'status', label: 'Status', minWidth: 100 },
  ];

  return (
    <Box>
      <PageHeader
        title="Products"
        subtitle="Manage your product catalog"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Inventory' },
          { label: 'Products' },
        ]}
        action={{
          label: 'Add Product',
          onClick: handleAddProduct,
          icon: <AddIcon />,
        }}
      />

      <DataTable
        columns={columns}
        rows={productData}
        title="Products"
        onEdit={handleEditProduct}
        onDelete={handleDeleteClick}
        onView={handleViewProduct}
        selectable={true}
        loading={isLoading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        totalCount={productData.length}
      />

      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete {selectedIds.length > 1 ? 'these products' : 'this product'}?
            This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} color="primary">
            Cancel
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Products;
