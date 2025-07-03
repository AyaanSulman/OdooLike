import React from 'react';
import { Navigate } from 'react-router-dom';

// Layouts
import MainLayout from '../layouts/MainLayout';
import AuthLayout from '../layouts/AuthLayout';

// Auth Pages
import Login from '../pages/auth/Login';
import Register from '../pages/auth/Register';

// Main Pages
import Dashboard from '../pages/Dashboard';
import NotFound from '../pages/NotFound';

// Inventory Pages
import Products from '../pages/inventory/Products';
import ProductDetail from '../pages/inventory/ProductDetail';
import Categories from '../pages/inventory/Categories';
import Warehouses from '../pages/inventory/Warehouses';
import StockLevels from '../pages/inventory/StockLevels';

// CRM Pages
import Contacts from '../pages/crm/Contacts';
import ContactDetail from '../pages/crm/ContactDetail';
import Leads from '../pages/crm/Leads';
import LeadDetail from '../pages/crm/LeadDetail';
import SalesPipeline from '../pages/crm/SalesPipeline';
import OpportunityDetail from '../pages/crm/OpportunityDetail';

interface RouteConfig {
  path: string;
  element: React.ReactNode;
  children?: RouteConfig[];
}

const routes: RouteConfig[] = [
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { path: '/', element: <Dashboard /> },
      
      // Inventory routes
      { path: '/inventory/products', element: <Products /> },
      { path: '/inventory/products/:id', element: <ProductDetail /> },
      { path: '/inventory/categories', element: <Categories /> },
      { path: '/inventory/warehouses', element: <Warehouses /> },
      { path: '/inventory/stock', element: <StockLevels /> },
      
      // CRM routes
      { path: '/crm/contacts', element: <Contacts /> },
      { path: '/crm/contacts/:id', element: <ContactDetail /> },
      { path: '/crm/contacts/:id/view', element: <ContactDetail /> },
      { path: '/crm/leads', element: <Leads /> },
      { path: '/crm/leads/:id', element: <LeadDetail /> },
      { path: '/crm/leads/:id/view', element: <LeadDetail /> },
      { path: '/crm/pipeline', element: <SalesPipeline /> },
      { path: '/crm/opportunities/:id', element: <OpportunityDetail /> },
      { path: '/crm/opportunities/:id/view', element: <OpportunityDetail /> },
      
      // Redirect root to dashboard
      { path: '', element: <Navigate to="/" /> },
      
      // 404 route
      { path: '*', element: <NotFound /> },
    ],
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <Login /> },
      { path: 'register', element: <Register /> },
      { path: '', element: <Navigate to="/auth/login" /> },
    ],
  },
];

export default routes;
