import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Box, CircularProgress } from '@mui/material';

// Layout components
import MainLayout from './components/layouts/MainLayout';
import AuthLayout from './components/layouts/AuthLayout';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import NotFound from './pages/NotFound';

// Inventory pages
import Products from './pages/inventory/Products';
import ProductDetail from './pages/inventory/ProductDetail';
import Categories from './pages/inventory/Categories';
import Warehouses from './pages/inventory/Warehouses';
import StockLevels from './pages/inventory/StockLevels';
import PurchaseOrders from './pages/inventory/PurchaseOrders';
import PurchaseOrderDetail from './pages/inventory/PurchaseOrderDetail';

// CRM pages
import Contacts from './pages/crm/Contacts';
import ContactDetail from './pages/crm/ContactDetail';
import Leads from './pages/crm/Leads';
import LeadDetail from './pages/crm/LeadDetail';
import SalesPipeline from './pages/crm/SalesPipeline';
import OpportunityDetail from './pages/crm/OpportunityDetail';

// Redux
import { RootState } from './store';
import { getCurrentUser } from './store/slices/authSlice';
import { AppDispatch } from './store';

// Protected Route component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useSelector((state: RootState) => state.auth);
  
  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

const App: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  
  useEffect(() => {
    if (isAuthenticated) {
      dispatch(getCurrentUser());
    }
  }, [dispatch, isAuthenticated]);
  
  return (
    <Routes>
      {/* Auth routes */}
      <Route path="/" element={<AuthLayout />}>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
      </Route>
      
      {/* Protected routes */}
      <Route path="/" element={
        <ProtectedRoute>
          <MainLayout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        
        {/* Inventory routes */}
        <Route path="inventory">
          <Route path="products" element={<Products />} />
          <Route path="products/:id" element={<ProductDetail />} />
          <Route path="categories" element={<Categories />} />
          <Route path="warehouses" element={<Warehouses />} />
          <Route path="stock-levels" element={<StockLevels />} />
          <Route path="purchase-orders" element={<PurchaseOrders />} />
          <Route path="purchase-orders/:id" element={<PurchaseOrderDetail />} />
        </Route>
        
        {/* CRM routes */}
        <Route path="crm">
          <Route path="contacts" element={<Contacts />} />
          <Route path="contacts/:id" element={<ContactDetail />} />
          <Route path="leads" element={<Leads />} />
          <Route path="leads/:id" element={<LeadDetail />} />
          <Route path="leads/:id/view" element={<LeadDetail />} />
          <Route path="pipeline" element={<SalesPipeline />} />
          <Route path="opportunities/:id" element={<OpportunityDetail />} />
          <Route path="opportunities/:id/view" element={<OpportunityDetail />} />
        </Route>
      </Route>
      
      {/* Not found route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;
