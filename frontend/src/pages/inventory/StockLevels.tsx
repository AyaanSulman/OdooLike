import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
  MenuItem,
  Grid,
  FormControl,
  InputLabel,
  Select,
  Typography,
  FormHelperText,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { fetchStockLevels, adjustStock } from '../../store/slices/inventorySlice';
import { fetchProducts } from '../../store/slices/inventorySlice';
import { fetchWarehouses } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';
import * as Yup from 'yup';
import { Formik, Form, Field } from 'formik';

interface StockAdjustmentFormValues {
  product_id: string;
  warehouse_id: string;
  quantity: number;
  reason: string;
  notes: string;
}

const StockLevels: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { stockLevels, products, warehouses, isLoading } = useSelector((state: RootState) => state.inventory);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [adjustDialogOpen, setAdjustDialogOpen] = useState(false);

  useEffect(() => {
    dispatch(fetchStockLevels());
    dispatch(fetchProducts());
    dispatch(fetchWarehouses());
  }, [dispatch]);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage: number) => {
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const handleAdjustDialogOpen = () => {
    setAdjustDialogOpen(true);
  };

  const handleAdjustDialogClose = () => {
    setAdjustDialogOpen(false);
  };

  // Mock data for demonstration
  const mockStockLevels = [
    {
      id: '1',
      product_name: 'Laptop XPS 15',
      product_sku: 'LAP-XPS-15',
      warehouse_name: 'Main Warehouse',
      warehouse_code: 'WH-MAIN',
      quantity: 15,
      min_stock_level: 5,
      status: 'In Stock',
      last_updated: '2023-06-15',
    },
    {
      id: '2',
      product_name: 'Wireless Mouse',
      product_sku: 'ACC-MOU-01',
      warehouse_name: 'Main Warehouse',
      warehouse_code: 'WH-MAIN',
      quantity: 45,
      min_stock_level: 10,
      status: 'In Stock',
      last_updated: '2023-06-10',
    },
    {
      id: '3',
      product_name: 'USB-C Cable',
      product_sku: 'CAB-USBC-01',
      warehouse_name: 'East Coast Distribution',
      warehouse_code: 'WH-EAST',
      quantity: 5,
      min_stock_level: 15,
      status: 'Low Stock',
      last_updated: '2023-06-12',
    },
    {
      id: '4',
      product_name: 'Monitor 27"',
      product_sku: 'MON-27-01',
      warehouse_name: 'West Coast Storage',
      warehouse_code: 'WH-WEST',
      quantity: 0,
      min_stock_level: 3,
      status: 'Out of Stock',
      last_updated: '2023-06-08',
    },
    {
      id: '5',
      product_name: 'Keyboard Mechanical',
      product_sku: 'KEY-MECH-01',
      warehouse_name: 'Main Warehouse',
      warehouse_code: 'WH-MAIN',
      quantity: 25,
      min_stock_level: 8,
      status: 'In Stock',
      last_updated: '2023-06-14',
    },
  ];

  const stockData = stockLevels?.length > 0 ? stockLevels : mockStockLevels;

  // Mock products and warehouses for the form
  const mockProductsData = [
    { id: '1', name: 'Laptop XPS 15', sku: 'LAP-XPS-15' },
    { id: '2', name: 'Wireless Mouse', sku: 'ACC-MOU-01' },
    { id: '3', name: 'USB-C Cable', sku: 'CAB-USBC-01' },
    { id: '4', name: 'Monitor 27"', sku: 'MON-27-01' },
    { id: '5', name: 'Keyboard Mechanical', sku: 'KEY-MECH-01' },
  ];

  const mockWarehousesData = [
    { id: '1', name: 'Main Warehouse', code: 'WH-MAIN' },
    { id: '2', name: 'East Coast Distribution', code: 'WH-EAST' },
    { id: '3', name: 'West Coast Storage', code: 'WH-WEST' },
  ];

  const productsData = products?.length > 0 ? products : mockProductsData;
  const warehousesData = warehouses?.length > 0 ? warehouses : mockWarehousesData;

  const columns = [
    { id: 'product_name', label: 'Product', minWidth: 180 },
    { id: 'product_sku', label: 'SKU', minWidth: 120 },
    { id: 'warehouse_name', label: 'Warehouse', minWidth: 150 },
    { id: 'warehouse_code', label: 'Warehouse Code', minWidth: 120 },
    {
      id: 'quantity',
      label: 'Quantity',
      minWidth: 100,
      align: 'right' as const,
    },
    {
      id: 'min_stock_level',
      label: 'Min Level',
      minWidth: 100,
      align: 'right' as const,
    },
    {
      id: 'status',
      label: 'Status',
      minWidth: 120,
      format: (value: string) => {
        let color;
        switch (value) {
          case 'In Stock':
            color = 'success.main';
            break;
          case 'Low Stock':
            color = 'warning.main';
            break;
          case 'Out of Stock':
            color = 'error.main';
            break;
          default:
            color = 'text.primary';
        }
        return <Typography sx={{ color }}>{value}</Typography>;
      },
    },
    { id: 'last_updated', label: 'Last Updated', minWidth: 120 },
  ];

  const validationSchema = Yup.object({
    product_id: Yup.string().required('Product is required'),
    warehouse_id: Yup.string().required('Warehouse is required'),
    quantity: Yup.number()
      .required('Quantity is required')
      .integer('Quantity must be an integer')
      .not([0], 'Quantity cannot be zero'),
    reason: Yup.string().required('Reason is required'),
  });

  const handleSubmit = async (values: StockAdjustmentFormValues) => {
    await dispatch(adjustStock(values));
    setAdjustDialogOpen(false);
  };

  return (
    <Box>
      <PageHeader
        title="Stock Levels"
        subtitle="Monitor and manage your inventory stock levels"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Inventory' },
          { label: 'Stock Levels' },
        ]}
        action={{
          label: 'Adjust Stock',
          onClick: handleAdjustDialogOpen,
          icon: <AddIcon />,
        }}
      />

      <DataTable
        columns={columns}
        rows={stockData}
        title="Stock Levels"
        loading={isLoading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        totalCount={stockData.length}
      />

      {/* Stock Adjustment Dialog */}
      <Dialog open={adjustDialogOpen} onClose={handleAdjustDialogClose} maxWidth="md" fullWidth>
        <DialogTitle>Adjust Stock</DialogTitle>
        <Formik
          initialValues={{
            product_id: '',
            warehouse_id: '',
            quantity: 0,
            reason: '',
            notes: '',
          }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ errors, touched, values, handleChange, handleBlur }) => (
            <Form>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth error={touched.product_id && Boolean(errors.product_id)}>
                      <InputLabel id="product-label">Product</InputLabel>
                      <Select
                        labelId="product-label"
                        id="product_id"
                        name="product_id"
                        value={values.product_id}
                        label="Product"
                        onChange={handleChange}
                        onBlur={handleBlur}
                      >
                        {productsData.map((product) => (
                          <MenuItem key={product.id} value={product.id}>
                            {product.name} ({product.sku})
                          </MenuItem>
                        ))}
                      </Select>
                      {touched.product_id && errors.product_id && (
                        <FormHelperText>{errors.product_id}</FormHelperText>
                      )}
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth error={touched.warehouse_id && Boolean(errors.warehouse_id)}>
                      <InputLabel id="warehouse-label">Warehouse</InputLabel>
                      <Select
                        labelId="warehouse-label"
                        id="warehouse_id"
                        name="warehouse_id"
                        value={values.warehouse_id}
                        label="Warehouse"
                        onChange={handleChange}
                        onBlur={handleBlur}
                      >
                        {warehousesData.map((warehouse) => (
                          <MenuItem key={warehouse.id} value={warehouse.id}>
                            {warehouse.name} ({warehouse.code})
                          </MenuItem>
                        ))}
                      </Select>
                      {touched.warehouse_id && errors.warehouse_id && (
                        <FormHelperText>{errors.warehouse_id}</FormHelperText>
                      )}
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="quantity"
                      name="quantity"
                      label="Quantity Adjustment"
                      type="number"
                      value={values.quantity}
                      onChange={handleChange}
                      onBlur={handleBlur}
                      error={touched.quantity && Boolean(errors.quantity)}
                      helperText={
                        (touched.quantity && errors.quantity) ||
                        'Use positive numbers for additions, negative for removals'
                      }
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth error={touched.reason && Boolean(errors.reason)}>
                      <InputLabel id="reason-label">Reason</InputLabel>
                      <Select
                        labelId="reason-label"
                        id="reason"
                        name="reason"
                        value={values.reason}
                        label="Reason"
                        onChange={handleChange}
                        onBlur={handleBlur}
                      >
                        <MenuItem value="purchase">Purchase</MenuItem>
                        <MenuItem value="sale">Sale</MenuItem>
                        <MenuItem value="return">Return</MenuItem>
                        <MenuItem value="damage">Damage/Loss</MenuItem>
                        <MenuItem value="transfer">Transfer</MenuItem>
                        <MenuItem value="adjustment">Inventory Adjustment</MenuItem>
                        <MenuItem value="other">Other</MenuItem>
                      </Select>
                      {touched.reason && errors.reason && <FormHelperText>{errors.reason}</FormHelperText>}
                    </FormControl>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      id="notes"
                      name="notes"
                      label="Notes"
                      multiline
                      rows={4}
                      value={values.notes}
                      onChange={handleChange}
                      onBlur={handleBlur}
                    />
                  </Grid>
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleAdjustDialogClose}>Cancel</Button>
                <Button type="submit" variant="contained" color="primary">
                  Adjust Stock
                </Button>
              </DialogActions>
            </Form>
          )}
        </Formik>
      </Dialog>
    </Box>
  );
};

export default StockLevels;
