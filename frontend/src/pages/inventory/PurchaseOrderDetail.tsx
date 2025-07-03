import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Box, Alert } from '@mui/material';
import { fetchPurchaseOrder, createPurchaseOrder, updatePurchaseOrder } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import FormikForm, { FormField } from '../../components/common/FormikForm';

interface PurchaseOrderFormValues {
  id?: string;
  po_number: string;
  supplier_id: string;
  order_date: string;
  expected_date: string;
  status: string;
  notes: string;
}

const PurchaseOrderDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { currentPurchaseOrder, isLoading, error } = useSelector((state: RootState) => state.inventory);
  const [initialValues, setInitialValues] = useState<PurchaseOrderFormValues>({
    po_number: '',
    supplier_id: '',
    order_date: '',
    expected_date: '',
    status: 'draft',
    notes: '',
  });

  const isNewPurchaseOrder = !id || id === 'new';

  useEffect(() => {
    if (!isNewPurchaseOrder && id) {
      dispatch(fetchPurchaseOrder(id));
    }
  }, [dispatch, id, isNewPurchaseOrder]);

  useEffect(() => {
    if (currentPurchaseOrder && !isNewPurchaseOrder) {
      setInitialValues({
        id: currentPurchaseOrder.id,
        po_number: currentPurchaseOrder.po_number || '',
        supplier_id: currentPurchaseOrder.supplier_id || '',
        order_date: currentPurchaseOrder.order_date || '',
        expected_date: currentPurchaseOrder.expected_date || '',
        status: currentPurchaseOrder.status || 'draft',
        notes: currentPurchaseOrder.notes || '',
      });
    }
  }, [currentPurchaseOrder, isNewPurchaseOrder]);

  const validationSchema = Yup.object({
    po_number: Yup.string().required('PO Number is required'),
    supplier_id: Yup.string().required('Supplier is required'),
    order_date: Yup.date().required('Order Date is required'),
    expected_date: Yup.date().required('Expected Date is required'),
    status: Yup.string().required('Status is required'),
    notes: Yup.string(),
  });

  const handleSubmit = async (values: PurchaseOrderFormValues) => {
    try {
      if (isNewPurchaseOrder) {
        await dispatch(createPurchaseOrder(values));
      } else {
        await dispatch(updatePurchaseOrder({ id: values.id!, data: values }));
      }
      navigate('/inventory/purchase-orders');
    } catch (error) {
      console.error('Error saving purchase order:', error);
    }
  };

  const handleCancel = () => {
    navigate('/inventory/purchase-orders');
  };

  const formSections = [
    {
      title: 'Purchase Order Information',
      fields: [
        {
          name: 'po_number',
          label: 'PO Number',
          type: 'text' as const,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'supplier_id',
          label: 'Supplier',
          type: 'select' as const,
          required: true,
          options: [
            { value: '1', label: 'Tech Supplies Inc.' },
            { value: '2', label: 'Office Equipment Co.' },
            { value: '3', label: 'Industrial Parts Ltd.' },
          ],
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'order_date',
          label: 'Order Date',
          type: 'date' as const,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'expected_date',
          label: 'Expected Date',
          type: 'date' as const,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'status',
          label: 'Status',
          type: 'select' as const,
          required: true,
          options: [
            { value: 'draft', label: 'Draft' },
            { value: 'sent', label: 'Sent' },
            { value: 'confirmed', label: 'Confirmed' },
            { value: 'cancelled', label: 'Cancelled' },
          ],
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'notes',
          label: 'Notes',
          type: 'textarea' as const,
          multiline: true,
          rows: 4,
          gridProps: { xs: 12 },
        },
      ] as FormField[],
    },
  ];

  return (
    <Box>
      <PageHeader
        title={isNewPurchaseOrder ? 'New Purchase Order' : 'Edit Purchase Order'}
        subtitle={isNewPurchaseOrder ? 'Create a new purchase order' : 'Update purchase order details'}
        breadcrumbs={[
          { label: 'Inventory', path: '/inventory' },
          { label: 'Purchase Orders', path: '/inventory/purchase-orders' },
          { label: isNewPurchaseOrder ? 'New' : 'Edit' },
        ]}
      />

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <FormikForm
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        sections={formSections}
        submitButtonText={isNewPurchaseOrder ? 'Create Purchase Order' : 'Update Purchase Order'}
        cancelButtonText="Cancel"
        onCancel={handleCancel}
        loading={isLoading}

      />
    </Box>
  );
};

export default PurchaseOrderDetail;
