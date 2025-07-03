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
  Grid,
  Paper,
  Typography,
  IconButton,
  Divider,
  Card,
  CardContent,
  CardActions,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Warehouse as WarehouseIcon,
  LocationOn as LocationIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';
import { fetchWarehouses, createWarehouse, updateWarehouse, deleteWarehouse } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import * as Yup from 'yup';
import { Formik, Form, Field } from 'formik';

interface WarehouseFormValues {
  id?: string;
  name: string;
  code: string;
  address: string;
  city: string;
  state: string;
  country: string;
  zip_code: string;
  is_active: boolean;
}

const Warehouses: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { warehouses, isLoading } = useSelector((state: RootState) => state.inventory);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [currentWarehouse, setCurrentWarehouse] = useState<WarehouseFormValues | null>(null);
  const [selectedWarehouseId, setSelectedWarehouseId] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchWarehouses());
  }, [dispatch]);

  // Mock warehouses for demonstration
  const mockWarehouses = [
    {
      id: '1',
      name: 'Main Warehouse',
      code: 'WH-MAIN',
      address: '123 Main Street',
      city: 'San Francisco',
      state: 'CA',
      country: 'USA',
      zip_code: '94105',
      is_active: true,
      product_count: 245,
      stock_value: 125000,
    },
    {
      id: '2',
      name: 'East Coast Distribution',
      code: 'WH-EAST',
      address: '456 Park Avenue',
      city: 'New York',
      state: 'NY',
      country: 'USA',
      zip_code: '10022',
      is_active: true,
      product_count: 189,
      stock_value: 98500,
    },
    {
      id: '3',
      name: 'West Coast Storage',
      code: 'WH-WEST',
      address: '789 Ocean Drive',
      city: 'Los Angeles',
      state: 'CA',
      country: 'USA',
      zip_code: '90210',
      is_active: true,
      product_count: 156,
      stock_value: 87300,
    },
  ];

  const warehouseData = warehouses?.length > 0 ? warehouses : mockWarehouses;

  const handleAddClick = () => {
    setCurrentWarehouse({
      name: '',
      code: '',
      address: '',
      city: '',
      state: '',
      country: '',
      zip_code: '',
      is_active: true,
    });
    setDialogOpen(true);
  };

  const handleEditClick = (warehouse: any) => {
    setCurrentWarehouse({
      id: warehouse.id,
      name: warehouse.name,
      code: warehouse.code,
      address: warehouse.address || '',
      city: warehouse.city || '',
      state: warehouse.state || '',
      country: warehouse.country || '',
      zip_code: warehouse.zip_code || '',
      is_active: warehouse.is_active !== false,
    });
    setDialogOpen(true);
  };

  const handleDeleteClick = (id: string) => {
    setSelectedWarehouseId(id);
    setDeleteDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setCurrentWarehouse(null);
  };

  const handleDeleteDialogClose = () => {
    setDeleteDialogOpen(false);
    setSelectedWarehouseId(null);
  };

  const handleDeleteConfirm = async () => {
    if (selectedWarehouseId) {
      await dispatch(deleteWarehouse(selectedWarehouseId));
      setDeleteDialogOpen(false);
      setSelectedWarehouseId(null);
    }
  };

  const validationSchema = Yup.object({
    name: Yup.string().required('Warehouse name is required'),
    code: Yup.string().required('Warehouse code is required'),
    address: Yup.string().required('Address is required'),
    city: Yup.string().required('City is required'),
    state: Yup.string().required('State is required'),
    country: Yup.string().required('Country is required'),
    zip_code: Yup.string().required('ZIP code is required'),
  });

  const handleSubmit = async (values: WarehouseFormValues) => {
    if (values.id) {
      await dispatch(updateWarehouse({ id: values.id, ...values }));
    } else {
      await dispatch(createWarehouse(values));
    }
    setDialogOpen(false);
    setCurrentWarehouse(null);
  };

  return (
    <Box>
      <PageHeader
        title="Warehouses"
        subtitle="Manage your warehouses and storage locations"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Inventory' },
          { label: 'Warehouses' },
        ]}
        action={{
          label: 'Add Warehouse',
          onClick: handleAddClick,
          icon: <AddIcon />,
        }}
      />

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {warehouseData.map((warehouse) => (
            <Grid item xs={12} md={6} lg={4} key={warehouse.id}>
              <Card sx={{ borderRadius: 2, height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <WarehouseIcon sx={{ mr: 1, color: 'primary.main' }} />
                      <Typography variant="h6">{warehouse.name}</Typography>
                    </Box>
                    <Chip
                      label={warehouse.code}
                      color="primary"
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                    <LocationIcon sx={{ mr: 1, fontSize: 18, color: 'text.secondary', mt: 0.3 }} />
                    <Typography variant="body2" color="text.secondary">
                      {warehouse.address}, {warehouse.city}, {warehouse.state} {warehouse.zip_code}, {warehouse.country}
                    </Typography>
                  </Box>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Products
                      </Typography>
                      <Typography variant="h6">{warehouse.product_count}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Stock Value
                      </Typography>
                      <Typography variant="h6">${warehouse.stock_value.toLocaleString()}</Typography>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    startIcon={<InventoryIcon />}
                    sx={{ mr: 'auto' }}
                  >
                    View Stock
                  </Button>
                  <IconButton size="small" onClick={() => handleEditClick(warehouse)}>
                    <EditIcon fontSize="small" />
                  </IconButton>
                  <IconButton size="small" onClick={() => handleDeleteClick(warehouse.id)}>
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Warehouse Form Dialog */}
      <Dialog open={dialogOpen} onClose={handleDialogClose} maxWidth="md" fullWidth>
        <DialogTitle>{currentWarehouse?.id ? 'Edit Warehouse' : 'Add Warehouse'}</DialogTitle>
        <Formik
          initialValues={{
            name: currentWarehouse?.name || '',
            code: currentWarehouse?.code || '',
            address: currentWarehouse?.address || '',
            city: currentWarehouse?.city || '',
            state: currentWarehouse?.state || '',
            country: currentWarehouse?.country || '',
            zip_code: currentWarehouse?.zip_code || '',
            is_active: currentWarehouse?.is_active !== false,
          }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ errors, touched }) => (
            <Form>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="name"
                      label="Warehouse Name"
                      fullWidth
                      variant="outlined"
                      error={touched.name && Boolean(errors.name)}
                      helperText={touched.name && errors.name}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="code"
                      label="Warehouse Code"
                      fullWidth
                      variant="outlined"
                      error={touched.code && Boolean(errors.code)}
                      helperText={touched.code && errors.code}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Field
                      as={TextField}
                      name="address"
                      label="Address"
                      fullWidth
                      variant="outlined"
                      error={touched.address && Boolean(errors.address)}
                      helperText={touched.address && errors.address}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="city"
                      label="City"
                      fullWidth
                      variant="outlined"
                      error={touched.city && Boolean(errors.city)}
                      helperText={touched.city && errors.city}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="state"
                      label="State/Province"
                      fullWidth
                      variant="outlined"
                      error={touched.state && Boolean(errors.state)}
                      helperText={touched.state && errors.state}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="zip_code"
                      label="ZIP/Postal Code"
                      fullWidth
                      variant="outlined"
                      error={touched.zip_code && Boolean(errors.zip_code)}
                      helperText={touched.zip_code && errors.zip_code}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Field
                      as={TextField}
                      name="country"
                      label="Country"
                      fullWidth
                      variant="outlined"
                      error={touched.country && Boolean(errors.country)}
                      helperText={touched.country && errors.country}
                    />
                  </Grid>
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleDialogClose}>Cancel</Button>
                <Button type="submit" variant="contained" color="primary">
                  {currentWarehouse?.id ? 'Update' : 'Create'}
                </Button>
              </DialogActions>
            </Form>
          )}
        </Formik>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={handleDeleteDialogClose}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this warehouse? This action cannot be undone and may affect
            inventory records associated with this warehouse.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteDialogClose}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Warehouses;
