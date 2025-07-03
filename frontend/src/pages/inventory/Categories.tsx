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
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Category as CategoryIcon,
} from '@mui/icons-material';
import { fetchCategories, createCategory, updateCategory, deleteCategory } from '../../store/slices/inventorySlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import * as Yup from 'yup';
import { Formik, Form, Field } from 'formik';

interface CategoryFormValues {
  id?: string;
  name: string;
  description: string;
  parent_id?: string | null;
}

const Categories: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { categories, isLoading } = useSelector((state: RootState) => state.inventory);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [currentCategory, setCurrentCategory] = useState<CategoryFormValues | null>(null);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchCategories());
  }, [dispatch]);

  // Mock categories for demonstration
  const mockCategories = [
    { id: '1', name: 'Electronics', description: 'Electronic devices and components', product_count: 45 },
    { id: '2', name: 'Accessories', description: 'Various accessories for devices', product_count: 78 },
    { id: '3', name: 'Cables', description: 'All types of cables and adapters', product_count: 32 },
    { id: '4', name: 'Office Supplies', description: 'Supplies for office use', product_count: 56 },
    { id: '5', name: 'Furniture', description: 'Office and home furniture', product_count: 18 },
  ];

  const categoryData = categories?.length > 0 ? categories : mockCategories;

  const handleAddClick = () => {
    setCurrentCategory({
      name: '',
      description: '',
      parent_id: null,
    });
    setDialogOpen(true);
  };

  const handleEditClick = (category: any) => {
    setCurrentCategory({
      id: category.id,
      name: category.name,
      description: category.description || '',
      parent_id: category.parent_id || null,
    });
    setDialogOpen(true);
  };

  const handleDeleteClick = (id: string) => {
    setSelectedCategoryId(id);
    setDeleteDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setCurrentCategory(null);
  };

  const handleDeleteDialogClose = () => {
    setDeleteDialogOpen(false);
    setSelectedCategoryId(null);
  };

  const handleDeleteConfirm = async () => {
    if (selectedCategoryId) {
      await dispatch(deleteCategory(selectedCategoryId));
      setDeleteDialogOpen(false);
      setSelectedCategoryId(null);
    }
  };

  const validationSchema = Yup.object({
    name: Yup.string().required('Category name is required'),
    description: Yup.string(),
  });

  const handleSubmit = async (values: CategoryFormValues) => {
    if (values.id) {
      await dispatch(updateCategory({ id: values.id, ...values }));
    } else {
      await dispatch(createCategory(values));
    }
    setDialogOpen(false);
    setCurrentCategory(null);
  };

  return (
    <Box>
      <PageHeader
        title="Categories"
        subtitle="Manage your product categories"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'Inventory' },
          { label: 'Categories' },
        ]}
        action={{
          label: 'Add Category',
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
          {categoryData.map((category) => (
            <Grid item xs={12} sm={6} md={4} key={category.id}>
              <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <CategoryIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6">{category.name}</Typography>
                  </Box>
                  <Box>
                    <IconButton size="small" onClick={() => handleEditClick(category)}>
                      <EditIcon fontSize="small" />
                    </IconButton>
                    <IconButton size="small" onClick={() => handleDeleteClick(category.id)}>
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Box>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {category.description}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="body2">
                  <strong>Products:</strong> {category.product_count}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Category Form Dialog */}
      <Dialog open={dialogOpen} onClose={handleDialogClose} maxWidth="sm" fullWidth>
        <DialogTitle>{currentCategory?.id ? 'Edit Category' : 'Add Category'}</DialogTitle>
        <Formik
          initialValues={{
            name: currentCategory?.name || '',
            description: currentCategory?.description || '',
            parent_id: currentCategory?.parent_id || null,
          }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ errors, touched }) => (
            <Form>
              <DialogContent>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Field
                      as={TextField}
                      name="name"
                      label="Category Name"
                      fullWidth
                      variant="outlined"
                      error={touched.name && Boolean(errors.name)}
                      helperText={touched.name && errors.name}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Field
                      as={TextField}
                      name="description"
                      label="Description"
                      fullWidth
                      variant="outlined"
                      multiline
                      rows={4}
                      error={touched.description && Boolean(errors.description)}
                      helperText={touched.description && errors.description}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Field
                      as={TextField}
                      select
                      name="parent_id"
                      label="Parent Category (Optional)"
                      fullWidth
                      variant="outlined"
                      SelectProps={{
                        native: true,
                      }}
                    >
                      <option value="">None</option>
                      {categoryData.map((cat) => (
                        // Don't show current category as parent option when editing
                        currentCategory?.id !== cat.id && (
                          <option key={cat.id} value={cat.id}>
                            {cat.name}
                          </option>
                        )
                      ))}
                    </Field>
                  </Grid>
                </Grid>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleDialogClose}>Cancel</Button>
                <Button type="submit" variant="contained" color="primary">
                  {currentCategory?.id ? 'Update' : 'Create'}
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
            Are you sure you want to delete this category? This action cannot be undone and may affect products
            assigned to this category.
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

export default Categories;
