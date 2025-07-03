import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  Inventory,
  People,
  ShoppingCart,
  Warning,
  ArrowForward,
  ArrowUpward,
  ArrowDownward,
} from '@mui/icons-material';
import { fetchInventoryStats, fetchLowStockProducts } from '../store/slices/inventorySlice';
import { fetchCrmStats } from '../store/slices/crmSlice';
import { RootState } from '../store';
import { AppDispatch } from '../store';
import PageHeader from '../components/common/PageHeader';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const { stats: inventoryStats, lowStockProducts, isLoading: inventoryLoading } = useSelector(
    (state: RootState) => state.inventory
  );
  const { stats: crmStats, isLoading: crmLoading } = useSelector((state: RootState) => state.crm);

  useEffect(() => {
    dispatch(fetchInventoryStats());
    dispatch(fetchLowStockProducts());
    dispatch(fetchCrmStats());
  }, [dispatch]);

  const isLoading = inventoryLoading || crmLoading;

  // Mock data for demonstration
  const mockInventoryStats = {
    total_products: 156,
    total_categories: 12,
    total_warehouses: 3,
    low_stock_count: 8,
    total_stock_value: 125000,
    recent_movements: 24,
  };

  const mockCrmStats = {
    total_contacts: 87,
    total_leads: 34,
    total_opportunities: 18,
    won_opportunities: 7,
    lost_opportunities: 3,
    conversion_rate: 38.9,
  };

  const stats = inventoryStats || mockInventoryStats;
  const crmStatsData = crmStats || mockCrmStats;

  const mockLowStockProducts = [
    { id: '1', name: 'Laptop XPS 15', sku: 'LAP-XPS-15', current_stock: 2, min_stock: 5 },
    { id: '2', name: 'Wireless Mouse', sku: 'ACC-MOU-01', current_stock: 3, min_stock: 10 },
    { id: '3', name: 'USB-C Cable', sku: 'CAB-USBC-01', current_stock: 5, min_stock: 15 },
  ];

  const lowStockItems = lowStockProducts?.length > 0 ? lowStockProducts : mockLowStockProducts;

  const StatCard = ({ title, value, icon, color, subtitle, change }: any) => (
    <Card sx={{ height: '100%', borderRadius: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            {title}
          </Typography>
          <Box
            sx={{
              backgroundColor: `${color}.lighter`,
              color: `${color}.main`,
              borderRadius: '50%',
              width: 40,
              height: 40,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {icon}
          </Box>
        </Box>
        <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
          {value}
        </Typography>
        {subtitle && (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {change && (
              <Box
                component="span"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  color: change >= 0 ? 'success.main' : 'error.main',
                  mr: 1,
                }}
              >
                {change >= 0 ? <ArrowUpward fontSize="small" /> : <ArrowDownward fontSize="small" />}
                {Math.abs(change)}%
              </Box>
            )}
            <Typography variant="body2" color="text.secondary">
              {subtitle}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <PageHeader
        title={`Welcome back, ${user?.first_name || 'User'}!`}
        subtitle="Here's what's happening with your business today."
      />

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Typography variant="h5" sx={{ mb: 3 }}>
            Inventory Overview
          </Typography>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Products"
                value={stats.total_products}
                icon={<Inventory />}
                color="primary"
                subtitle="Across all categories"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Stock Value"
                value={`$${stats.total_stock_value.toLocaleString()}`}
                icon={<TrendingUp />}
                color="success"
                subtitle="Current inventory value"
                change={2.5}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Low Stock Items"
                value={stats.low_stock_count}
                icon={<Warning />}
                color="warning"
                subtitle="Items below minimum level"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Recent Movements"
                value={stats.recent_movements}
                icon={<ShoppingCart />}
                color="info"
                subtitle="In the last 24 hours"
              />
            </Grid>
          </Grid>

          <Typography variant="h5" sx={{ mb: 3 }}>
            CRM Overview
          </Typography>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Total Contacts"
                value={crmStatsData.total_contacts}
                icon={<People />}
                color="primary"
                subtitle="Active contacts"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Active Leads"
                value={crmStatsData.total_leads}
                icon={<TrendingUp />}
                color="info"
                subtitle="Potential opportunities"
                change={4.2}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Opportunities"
                value={crmStatsData.total_opportunities}
                icon={<TrendingUp />}
                color="success"
                subtitle="In sales pipeline"
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Conversion Rate"
                value={`${crmStatsData.conversion_rate}%`}
                icon={<TrendingUp />}
                color="success"
                subtitle="Lead to opportunity"
                change={1.8}
              />
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Low Stock Products
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List>
                  {lowStockItems.map((product) => (
                    <ListItem key={product.id} divider>
                      <ListItemIcon>
                        <Warning color="warning" />
                      </ListItemIcon>
                      <ListItemText
                        primary={product.name}
                        secondary={`SKU: ${product.sku} | Current Stock: ${product.current_stock} | Min Stock: ${product.min_stock}`}
                      />
                    </ListItem>
                  ))}
                </List>
                <CardActions>
                  <Button
                    size="small"
                    endIcon={<ArrowForward />}
                    component={RouterLink}
                    to="/inventory/stock-levels"
                  >
                    View All Stock Levels
                  </Button>
                </CardActions>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Recent Activities
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <List>
                  <ListItem divider>
                    <ListItemText
                      primary="New purchase order created"
                      secondary="PO-2023-001 | Created by John Doe | 2 hours ago"
                    />
                  </ListItem>
                  <ListItem divider>
                    <ListItemText
                      primary="Stock adjustment approved"
                      secondary="ADJ-2023-005 | Approved by Jane Smith | 3 hours ago"
                    />
                  </ListItem>
                  <ListItem divider>
                    <ListItemText
                      primary="New lead assigned"
                      secondary="Acme Corp | Assigned to Sales Team | 5 hours ago"
                    />
                  </ListItem>
                </List>
                <CardActions>
                  <Button size="small" endIcon={<ArrowForward />}>
                    View All Activities
                  </Button>
                </CardActions>
              </Paper>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
};

export default Dashboard;
