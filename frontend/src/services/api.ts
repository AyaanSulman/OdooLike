import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Generic API request function with type safety
export const apiRequest = async <T>(
  method: string,
  url: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<T> => {
  try {
    const response: AxiosResponse<T> = await api({
      method,
      url,
      data,
      ...config,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError<{ detail: string }>;
      if (serverError && serverError.response) {
        throw new Error(serverError.response.data.detail || 'An error occurred');
      }
    }
    throw new Error('Network error');
  }
};

// API service with typed methods
const apiService = {
  // Auth endpoints
  login: (credentials: { email: string; password: string }) =>
    apiRequest<{ token: string; user: any }>('post', '/auth/login/', credentials),
  
  register: (userData: any) =>
    apiRequest<{ token: string; user: any }>('post', '/auth/register/', userData),
  
  getCurrentUser: () =>
    apiRequest<any>('get', '/auth/me/'),
  
  // CRM endpoints
  getContacts: (params?: any) =>
    apiRequest<any>('get', '/crm/contacts/', undefined, { params }),
  
  getContact: (id: string) =>
    apiRequest<any>('get', `/crm/contacts/${id}/`),
  
  createContact: (data: any) =>
    apiRequest<any>('post', '/crm/contacts/', data),
  
  updateContact: (id: string, data: any) =>
    apiRequest<any>('put', `/crm/contacts/${id}/`, data),
  
  deleteContact: (id: string) =>
    apiRequest<any>('delete', `/crm/contacts/${id}/`),
  
  getLeads: (params?: any) =>
    apiRequest<any>('get', '/crm/leads/', undefined, { params }),
  
  getLead: (id: string) =>
    apiRequest<any>('get', `/crm/leads/${id}/`),
  
  createLead: (data: any) =>
    apiRequest<any>('post', '/crm/leads/', data),
  
  updateLead: (id: string, data: any) =>
    apiRequest<any>('put', `/crm/leads/${id}/`, data),
  
  deleteLead: (id: string) =>
    apiRequest<any>('delete', `/crm/leads/${id}/`),
  
  convertLead: (id: string, data: any) =>
    apiRequest<any>('post', `/crm/leads/${id}/convert/`, data),
  
  getOpportunities: (params?: any) =>
    apiRequest<any>('get', '/crm/opportunities/', undefined, { params }),
  
  getOpportunity: (id: string) =>
    apiRequest<any>('get', `/crm/opportunities/${id}/`),
  
  createOpportunity: (data: any) =>
    apiRequest<any>('post', '/crm/opportunities/', data),
  
  updateOpportunity: (id: string, data: any) =>
    apiRequest<any>('put', `/crm/opportunities/${id}/`, data),
  
  deleteOpportunity: (id: string) =>
    apiRequest<any>('delete', `/crm/opportunities/${id}/`),
  
  updateOpportunityStage: (id: string, data: any) =>
    apiRequest<any>('post', `/crm/opportunities/${id}/update-stage/`, data),
  
  getCrmStats: () =>
    apiRequest<any>('get', '/crm/stats/'),
  
  // Inventory endpoints
  getProducts: (params?: any) =>
    apiRequest<any>('get', '/inventory/products/', undefined, { params }),
  
  getProduct: (id: string) =>
    apiRequest<any>('get', `/inventory/products/${id}/`),
  
  createProduct: (data: any) =>
    apiRequest<any>('post', '/inventory/products/', data),
  
  updateProduct: (id: string, data: any) =>
    apiRequest<any>('put', `/inventory/products/${id}/`, data),
  
  deleteProduct: (id: string) =>
    apiRequest<any>('delete', `/inventory/products/${id}/`),
  
  getProductStockHistory: (id: string) =>
    apiRequest<any>('get', `/inventory/products/${id}/stock-history/`),
  
  getCategories: (params?: any) =>
    apiRequest<any>('get', '/inventory/categories/', undefined, { params }),
  
  getCategory: (id: string) =>
    apiRequest<any>('get', `/inventory/categories/${id}/`),
  
  createCategory: (data: any) =>
    apiRequest<any>('post', '/inventory/categories/', data),
  
  updateCategory: (id: string, data: any) =>
    apiRequest<any>('put', `/inventory/categories/${id}/`, data),
  
  deleteCategory: (id: string) =>
    apiRequest<any>('delete', `/inventory/categories/${id}/`),
  
  getWarehouses: (params?: any) =>
    apiRequest<any>('get', '/inventory/warehouses/', undefined, { params }),
  
  getWarehouse: (id: string) =>
    apiRequest<any>('get', `/inventory/warehouses/${id}/`),
  
  createWarehouse: (data: any) =>
    apiRequest<any>('post', '/inventory/warehouses/', data),
  
  updateWarehouse: (id: string, data: any) =>
    apiRequest<any>('put', `/inventory/warehouses/${id}/`, data),
  
  deleteWarehouse: (id: string) =>
    apiRequest<any>('delete', `/inventory/warehouses/${id}/`),
  
  getStockLevels: (params?: any) =>
    apiRequest<any>('get', '/inventory/stock-levels/', undefined, { params }),
  
  createStockMovement: (data: any) =>
    apiRequest<any>('post', '/inventory/stock-movements/create/', data),
  
  bulkUpdateStock: (data: any) =>
    apiRequest<any>('post', '/inventory/stock-movements/bulk-update/', data),
  
  getPurchaseOrders: (params?: any) =>
    apiRequest<any>('get', '/inventory/purchase-orders/', undefined, { params }),
  
  getPurchaseOrder: (id: string) =>
    apiRequest<any>('get', `/inventory/purchase-orders/${id}/`),
  
  createPurchaseOrder: (data: any) =>
    apiRequest<any>('post', '/inventory/purchase-orders/', data),
  
  updatePurchaseOrder: (id: string, data: any) =>
    apiRequest<any>('put', `/inventory/purchase-orders/${id}/`, data),
  
  deletePurchaseOrder: (id: string) =>
    apiRequest<any>('delete', `/inventory/purchase-orders/${id}/`),
  
  getInventoryStats: () =>
    apiRequest<any>('get', '/inventory/stats/'),
  
  getLowStockProducts: () => apiRequest<any[]>('GET', '/inventory/low-stock'),
  adjustStock: (productId: string, adjustment: number, reason: string) => 
    apiRequest<any>('POST', `/inventory/products/${productId}/adjust-stock`, { adjustment, reason }),
};

export default apiService;
