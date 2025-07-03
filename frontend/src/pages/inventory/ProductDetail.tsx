import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Box, Typography, Alert } from '@mui/material';
import { fetchProductById, createProduct, updateProduct } from '../../store/slices/inventorySlice';
import { fetchCategories } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import FormikForm, { FormField } from '../../components/common/FormikForm';

const ProductDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isNewProduct = id === 'new';
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { product, categories, isLoading, error } = useSelector((state: RootState) => state.inventory);
  const [initialValues, setInitialValues] = useState({
    name: '',
    sku: '',
    description: '',
    category_id: '',
    price: '',
    cost: '',
    min_stock_level: '',
    tax_rate: '',
    weight: '',
    dimensions: '',
    barcode: '',
    is_active: true,
  });

  useEffect(() => {
    dispatch(fetchCategories());
    if (!isNewProduct && id) {
      dispatch(fetchProductById(id));
    }
  }, [dispatch, id, isNewProduct]);

  useEffect(() => {
    if (!isNewProduct && product) {
      setInitialValues({
        name: product.name || '',
        sku: product.sku || '',
        description: product.description || '',
        category_id: product.category_id || '',
        price: product.price?.toString() || '',
        cost: product.cost?.toString() || '',
        min_stock_level: product.min_stock_level?.toString() || '',
        tax_rate: product.tax_rate?.toString() || '',
        weight: product.weight?.toString() || '',
        dimensions: product.dimensions || '',
        barcode: product.barcode || '',
        is_active: product.is_active !== false,
      });
    }
  }, [product, isNewProduct]);

  // Mock categories for demonstration
  const mockCategories = [
    { id: '1', name: 'Electronics' },
    { id: '2', name: 'Accessories' },
    { id: '3', name: 'Cables' },
    { id: '4', name: 'Office Supplies' },
    { id: '5', name: 'Furniture' },
  ];

  const categoryOptions = (categories?.length > 0 ? categories : mockCategories).map((category) => ({
    value: category.id,
    label: category.name,
  }));

  const validationSchema = Yup.object({
    name: Yup.string().required('Product name is required'),
    sku: Yup.string().required('SKU is required'),
    category_id: Yup.string().required('Category is required'),
    price: Yup.number().typeError('Price must be a number').required('Price is required').min(0, 'Price must be positive'),
    cost: Yup.number().typeError('Cost must be a number').required('Cost is required').min(0, 'Cost must be positive'),
    min_stock_level: Yup.number()
      .typeError('Minimum stock level must be a number')
      .integer('Minimum stock level must be an integer')
      .min(0, 'Minimum stock level must be positive'),
    tax_rate: Yup.number().typeError('Tax rate must be a number').min(0, 'Tax rate must be positive'),
  });

  const handleSubmit = async (values: any) => {
    const productData = {
      ...values,
      price: parseFloat(values.price),
      cost: parseFloat(values.cost),
      min_stock_level: parseInt(values.min_stock_level, 10),
      tax_rate: values.tax_rate ? parseFloat(values.tax_rate) : 0,
      weight: values.weight ? parseFloat(values.weight) : null,
    };

    if (isNewProduct) {
      await dispatch(createProduct(productData));
    } else if (id) {
      await dispatch(updateProduct({ id, ...productData }));
    }

    navigate('/inventory/products');
  };

  const handleCancel = () => {
    navigate('/inventory/products');
  };

  const formSections = [
    {
      title: 'Basic Information',
      fields: [
        {
          name: 'name',
          label: 'Product Name',
          type: 'text',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'sku',
          label: 'SKU',
          type: 'text',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'category_id',
          label: 'Category',
          type: 'select',
          options: categoryOptions,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'barcode',
          label: 'Barcode',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'description',
          label: 'Description',
          type: 'textarea',
          multiline: true,
          rows: 4,
          gridProps: { xs: 12 },
        },
      ],
    },
    {
      title: 'Pricing and Inventory',
      fields: [
        {
          name: 'price',
          label: 'Sales Price',
          type: 'number',
          required: true,
          gridProps: { xs: 12, sm: 6, md: 3 },
        },
        {
          name: 'cost',
          label: 'Cost Price',
          type: 'number',
          required: true,
          gridProps: { xs: 12, sm: 6, md: 3 },
        },
        {
          name: 'tax_rate',
          label: 'Tax Rate (%)',
          type: 'number',
          gridProps: { xs: 12, sm: 6, md: 3 },
        },
        {
          name: 'min_stock_level',
          label: 'Minimum Stock Level',
          type: 'number',
          gridProps: { xs: 12, sm: 6, md: 3 },
        },
      ],
    },
    {
      title: 'Physical Properties',
      fields: [
        {
          name: 'weight',
          label: 'Weight (kg)',
          type: 'number',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'dimensions',
          label: 'Dimensions (LxWxH)',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'is_active',
          label: 'Active Product',
          type: 'checkbox',
          gridProps: { xs: 12 },
        },
      ],
    },
  ];

  return (
    <Box>
      <PageHeader
        title={isNewProduct ? 'Add New Product' : 'Edit Product'}
        subtitle={isNewProduct ? 'Create a new product in your inventory' : 'Update product details'}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Inventory', path: '/inventory' },
          { label: 'Products', path: '/inventory/products' },
          { label: isNewProduct ? 'Add New' : 'Edit' },
        ]}
      />

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <FormikForm
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        sections={formSections}
        submitButtonText={isNewProduct ? 'Create Product' : 'Update Product'}
        cancelButtonText="Cancel"
        onCancel={handleCancel}
        loading={isLoading}
        error={error}
      />
    </Box>
  );
};

export default ProductDetail;
