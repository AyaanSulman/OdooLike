import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../../services/api';

interface InventoryState {
  products: any[];
  categories: any[];
  brands: any[];
  suppliers: any[];
  warehouses: any[];
  stockLevels: any[];
  purchaseOrders: any[];
  stats: any;
  lowStockProducts: any[];
  currentProduct: any | null;
  currentCategory: any | null;
  currentWarehouse: any | null;
  currentPurchaseOrder: any | null;
  productStockHistory: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: InventoryState = {
  products: [],
  categories: [],
  brands: [],
  suppliers: [],
  warehouses: [],
  stockLevels: [],
  purchaseOrders: [],
  stats: null,
  lowStockProducts: [],
  currentProduct: null,
  currentCategory: null,
  currentWarehouse: null,
  currentPurchaseOrder: null,
  productStockHistory: [],
  isLoading: false,
  error: null,
};

// Products
export const fetchProducts = createAsyncThunk(
  'inventory/fetchProducts',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getProducts(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch products');
    }
  }
);

export const fetchProduct = createAsyncThunk(
  'inventory/fetchProduct',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getProduct(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch product');
    }
  }
);

export const createProduct = createAsyncThunk(
  'inventory/createProduct',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createProduct(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create product');
    }
  }
);

export const updateProduct = createAsyncThunk(
  'inventory/updateProduct',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateProduct(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update product');
    }
  }
);

export const deleteProduct = createAsyncThunk(
  'inventory/deleteProduct',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteProduct(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete product');
    }
  }
);

export const fetchProductStockHistory = createAsyncThunk(
  'inventory/fetchProductStockHistory',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getProductStockHistory(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch product stock history');
    }
  }
);

// Categories
export const fetchCategories = createAsyncThunk(
  'inventory/fetchCategories',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getCategories(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch categories');
    }
  }
);

export const fetchCategory = createAsyncThunk(
  'inventory/fetchCategory',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getCategory(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch category');
    }
  }
);

export const createCategory = createAsyncThunk(
  'inventory/createCategory',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createCategory(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create category');
    }
  }
);

export const updateCategory = createAsyncThunk(
  'inventory/updateCategory',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateCategory(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update category');
    }
  }
);

export const deleteCategory = createAsyncThunk(
  'inventory/deleteCategory',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteCategory(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete category');
    }
  }
);

// Warehouses
export const fetchWarehouses = createAsyncThunk(
  'inventory/fetchWarehouses',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getWarehouses(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch warehouses');
    }
  }
);

export const fetchWarehouse = createAsyncThunk(
  'inventory/fetchWarehouse',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getWarehouse(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch warehouse');
    }
  }
);

export const createWarehouse = createAsyncThunk(
  'inventory/createWarehouse',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createWarehouse(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create warehouse');
    }
  }
);

export const updateWarehouse = createAsyncThunk(
  'inventory/updateWarehouse',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateWarehouse(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update warehouse');
    }
  }
);

export const deleteWarehouse = createAsyncThunk(
  'inventory/deleteWarehouse',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteWarehouse(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete warehouse');
    }
  }
);

// Stock Levels
export const fetchStockLevels = createAsyncThunk(
  'inventory/fetchStockLevels',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getStockLevels(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch stock levels');
    }
  }
);

export const createStockMovement = createAsyncThunk(
  'inventory/createStockMovement',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createStockMovement(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create stock movement');
    }
  }
);

export const bulkUpdateStock = createAsyncThunk(
  'inventory/bulkUpdateStock',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.bulkUpdateStock(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to bulk update stock');
    }
  }
);

// Purchase Orders
export const fetchPurchaseOrders = createAsyncThunk(
  'inventory/fetchPurchaseOrders',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getPurchaseOrders(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch purchase orders');
    }
  }
);

export const fetchPurchaseOrder = createAsyncThunk(
  'inventory/fetchPurchaseOrder',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getPurchaseOrder(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch purchase order');
    }
  }
);

export const createPurchaseOrder = createAsyncThunk(
  'inventory/createPurchaseOrder',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createPurchaseOrder(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create purchase order');
    }
  }
);

export const updatePurchaseOrder = createAsyncThunk(
  'inventory/updatePurchaseOrder',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updatePurchaseOrder(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update purchase order');
    }
  }
);

export const deletePurchaseOrder = createAsyncThunk(
  'inventory/deletePurchaseOrder',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deletePurchaseOrder(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete purchase order');
    }
  }
);

// Stats
export const fetchInventoryStats = createAsyncThunk(
  'inventory/fetchInventoryStats',
  async (_, { rejectWithValue }) => {
    try {
      return await apiService.getInventoryStats();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch inventory stats');
    }
  }
);

export const fetchLowStockProducts = createAsyncThunk(
  'inventory/fetchLowStockProducts',
  async (_, { rejectWithValue }) => {
    try {
      return await apiService.getLowStockProducts();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch low stock products');
    }
  }
);

export const adjustStock = createAsyncThunk(
  'inventory/adjustStock',
  async ({ productId, adjustment, reason }: { productId: string; adjustment: number; reason: string }, { rejectWithValue }) => {
    try {
      return await apiService.adjustStock(productId, adjustment, reason);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to adjust stock');
    }
  }
);

const inventorySlice = createSlice({
  name: 'inventory',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentProduct: (state) => {
      state.currentProduct = null;
    },
    clearCurrentCategory: (state) => {
      state.currentCategory = null;
    },
    clearCurrentWarehouse: (state) => {
      state.currentWarehouse = null;
    },
    clearCurrentPurchaseOrder: (state) => {
      state.currentPurchaseOrder = null;
    },
  },
  extraReducers: (builder) => {
    // Products
    builder.addCase(fetchProducts.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchProducts.fulfilled, (state, action) => {
      state.isLoading = false;
      state.products = action.payload.results || action.payload;
    });
    builder.addCase(fetchProducts.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchProduct.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchProduct.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentProduct = action.payload;
    });
    builder.addCase(fetchProduct.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(createProduct.fulfilled, (state, action) => {
      state.products.push(action.payload);
    });

    builder.addCase(updateProduct.fulfilled, (state, action) => {
      const index = state.products.findIndex((product) => product.id === action.payload.id);
      if (index !== -1) {
        state.products[index] = action.payload;
      }
      state.currentProduct = action.payload;
    });

    builder.addCase(deleteProduct.fulfilled, (state, action) => {
      state.products = state.products.filter((product) => product.id !== action.payload);
      if (state.currentProduct && state.currentProduct.id === action.payload) {
        state.currentProduct = null;
      }
    });

    builder.addCase(fetchProductStockHistory.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchProductStockHistory.fulfilled, (state, action) => {
      state.isLoading = false;
      state.productStockHistory = action.payload;
    });
    builder.addCase(fetchProductStockHistory.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    // Categories
    builder.addCase(fetchCategories.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchCategories.fulfilled, (state, action) => {
      state.isLoading = false;
      state.categories = action.payload.results || action.payload;
    });
    builder.addCase(fetchCategories.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchCategory.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchCategory.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentCategory = action.payload;
    });
    builder.addCase(fetchCategory.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    // Warehouses
    builder.addCase(fetchWarehouses.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchWarehouses.fulfilled, (state, action) => {
      state.isLoading = false;
      state.warehouses = action.payload.results || action.payload;
    });
    builder.addCase(fetchWarehouses.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchWarehouse.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchWarehouse.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentWarehouse = action.payload;
    });
    builder.addCase(fetchWarehouse.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    // Stock Levels
    builder.addCase(fetchStockLevels.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchStockLevels.fulfilled, (state, action) => {
      state.isLoading = false;
      state.stockLevels = action.payload.results || action.payload;
    });
    builder.addCase(fetchStockLevels.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    // Purchase Orders
    builder.addCase(fetchPurchaseOrders.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchPurchaseOrders.fulfilled, (state, action) => {
      state.isLoading = false;
      state.purchaseOrders = action.payload.results || action.payload;
    });
    builder.addCase(fetchPurchaseOrders.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchPurchaseOrder.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchPurchaseOrder.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentPurchaseOrder = action.payload;
    });
    builder.addCase(fetchPurchaseOrder.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    // Stats
    builder.addCase(fetchInventoryStats.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchInventoryStats.fulfilled, (state, action) => {
      state.isLoading = false;
      state.stats = action.payload;
    });
    builder.addCase(fetchInventoryStats.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchLowStockProducts.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchLowStockProducts.fulfilled, (state, action) => {
      state.isLoading = false;
      state.lowStockProducts = action.payload;
    });
    builder.addCase(fetchLowStockProducts.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });
  },
});

export const {
  clearError,
  clearCurrentProduct,
  clearCurrentCategory,
  clearCurrentWarehouse,
  clearCurrentPurchaseOrder,
} = inventorySlice.actions;

export default inventorySlice.reducer;
