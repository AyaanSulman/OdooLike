import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Chip,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { fetchPurchaseOrders, deletePurchaseOrder } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';

const PurchaseOrders: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { purchaseOrders, isLoading } = useSelector((state: RootState) => state.inventory);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedPurchaseOrder, setSelectedPurchaseOrder] = useState<any>(null);

  useEffect(() => {
    dispatch(fetchPurchaseOrders({}));
  }, [dispatch]);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage: number) => {
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const handleAddPurchaseOrder = () => {
    navigate('/inventory/purchase-orders/new');
  };

  const handleEditPurchaseOrder = (id: string) => {
    navigate(`/inventory/purchase-orders/${id}`);
  };

  const handleViewPurchaseOrder = (id: string) => {
    navigate(`/inventory/purchase-orders/${id}/view`);
  };

  const handleDeletePurchaseOrder = (purchaseOrder: any) => {
    setSelectedPurchaseOrder(purchaseOrder);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (selectedPurchaseOrder) {
      await dispatch(deletePurchaseOrder(selectedPurchaseOrder.id));
      setDeleteDialogOpen(false);
      setSelectedPurchaseOrder(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft':
        return 'default';
      case 'sent':
        return 'info';
      case 'confirmed':
        return 'success';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const columns = [
    { id: 'po_number', label: 'PO Number', minWidth: 120 },
    { id: 'supplier_name', label: 'Supplier', minWidth: 150 },
    {
      id: 'status',
      label: 'Status',
      minWidth: 100,
      format: (value: string) => value.charAt(0).toUpperCase() + value.slice(1),
    },
    { id: 'order_date', label: 'Order Date', minWidth: 120 },
    { id: 'expected_date', label: 'Expected Date', minWidth: 120 },
    {
      id: 'total_amount',
      label: 'Total Amount',
      minWidth: 120,
      align: 'right' as const,
      format: (value: number) => `$${value.toFixed(2)}`,
    },
  ];

  // Mock data for demonstration
  const purchaseOrderData = [
    {
      id: '1',
      po_number: 'PO-2023-001',
      supplier_name: 'Tech Supplies Inc.',
      status: 'confirmed',
      order_date: '2023-12-01',
      expected_date: '2023-12-15',
      total_amount: 2500.00,
    },
    {
      id: '2',
      po_number: 'PO-2023-002',
      supplier_name: 'Office Equipment Co.',
      status: 'sent',
      order_date: '2023-12-02',
      expected_date: '2023-12-16',
      total_amount: 1800.50,
    },
  ];

  return (
    <Box>
      <PageHeader
        title="Purchase Orders"
        subtitle="Manage your purchase orders and supplier relationships"
        breadcrumbs={[
          { label: 'Inventory', path: '/inventory' },
          { label: 'Purchase Orders' },
        ]}
        action={{
          label: 'New Purchase Order',
          onClick: handleAddPurchaseOrder,
          icon: <AddIcon />
        }}
      />

      <DataTable
        columns={columns}
        rows={purchaseOrderData}
        title="Purchase Orders"
        onEdit={handleEditPurchaseOrder}
        onView={handleViewPurchaseOrder}
        onDelete={handleDeletePurchaseOrder}
        loading={isLoading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        totalCount={purchaseOrderData.length}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Purchase Order</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete purchase order "{selectedPurchaseOrder?.po_number}"?
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={confirmDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PurchaseOrders;
