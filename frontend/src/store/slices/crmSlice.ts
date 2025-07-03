import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import apiService from '../../services/api';

interface CrmState {
  contacts: any[];
  leads: any[];
  opportunities: any[];
  campaigns: any[];
  salesStages: any[];
  stats: any;
  currentContact: any | null;
  currentLead: any | null;
  currentOpportunity: any | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: CrmState = {
  contacts: [],
  leads: [],
  opportunities: [],
  campaigns: [],
  salesStages: [],
  stats: null,
  currentContact: null,
  currentLead: null,
  currentOpportunity: null,
  isLoading: false,
  error: null,
};

// Contacts
export const fetchContacts = createAsyncThunk(
  'crm/fetchContacts',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getContacts(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch contacts');
    }
  }
);

export const fetchContact = createAsyncThunk(
  'crm/fetchContact',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getContact(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch contact');
    }
  }
);

export const createContact = createAsyncThunk(
  'crm/createContact',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createContact(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create contact');
    }
  }
);

export const updateContact = createAsyncThunk(
  'crm/updateContact',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateContact(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update contact');
    }
  }
);

export const deleteContact = createAsyncThunk(
  'crm/deleteContact',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteContact(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete contact');
    }
  }
);

// Leads
export const fetchLeads = createAsyncThunk(
  'crm/fetchLeads',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getLeads(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch leads');
    }
  }
);

export const fetchLead = createAsyncThunk(
  'crm/fetchLead',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getLead(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch lead');
    }
  }
);

export const createLead = createAsyncThunk(
  'crm/createLead',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createLead(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create lead');
    }
  }
);

export const updateLead = createAsyncThunk(
  'crm/updateLead',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateLead(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update lead');
    }
  }
);

export const deleteLead = createAsyncThunk(
  'crm/deleteLead',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteLead(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete lead');
    }
  }
);

export const convertLead = createAsyncThunk(
  'crm/convertLead',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.convertLead(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to convert lead');
    }
  }
);

// Opportunities
export const fetchOpportunities = createAsyncThunk(
  'crm/fetchOpportunities',
  async (params: any = {}, { rejectWithValue }) => {
    try {
      return await apiService.getOpportunities(params);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch opportunities');
    }
  }
);

export const fetchOpportunity = createAsyncThunk(
  'crm/fetchOpportunity',
  async (id: string, { rejectWithValue }) => {
    try {
      return await apiService.getOpportunity(id);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch opportunity');
    }
  }
);

export const createOpportunity = createAsyncThunk(
  'crm/createOpportunity',
  async (data: any, { rejectWithValue }) => {
    try {
      return await apiService.createOpportunity(data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to create opportunity');
    }
  }
);

export const updateOpportunity = createAsyncThunk(
  'crm/updateOpportunity',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateOpportunity(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update opportunity');
    }
  }
);

export const deleteOpportunity = createAsyncThunk(
  'crm/deleteOpportunity',
  async (id: string, { rejectWithValue }) => {
    try {
      await apiService.deleteOpportunity(id);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to delete opportunity');
    }
  }
);

export const updateOpportunityStage = createAsyncThunk(
  'crm/updateOpportunityStage',
  async ({ id, data }: { id: string; data: any }, { rejectWithValue }) => {
    try {
      return await apiService.updateOpportunityStage(id, data);
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to update opportunity stage');
    }
  }
);

// Stats
export const fetchCrmStats = createAsyncThunk(
  'crm/fetchCrmStats',
  async (_, { rejectWithValue }) => {
    try {
      return await apiService.getCrmStats();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch CRM stats');
    }
  }
);

const crmSlice = createSlice({
  name: 'crm',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentContact: (state) => {
      state.currentContact = null;
    },
    clearCurrentLead: (state) => {
      state.currentLead = null;
    },
    clearCurrentOpportunity: (state) => {
      state.currentOpportunity = null;
    },
  },
  extraReducers: (builder) => {
    // Contacts
    builder.addCase(fetchContacts.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchContacts.fulfilled, (state, action) => {
      state.isLoading = false;
      state.contacts = action.payload.results || action.payload;
    });
    builder.addCase(fetchContacts.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchContact.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchContact.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentContact = action.payload;
    });
    builder.addCase(fetchContact.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(createContact.fulfilled, (state, action) => {
      state.contacts.push(action.payload);
    });

    builder.addCase(updateContact.fulfilled, (state, action) => {
      const index = state.contacts.findIndex((contact) => contact.id === action.payload.id);
      if (index !== -1) {
        state.contacts[index] = action.payload;
      }
      state.currentContact = action.payload;
    });

    builder.addCase(deleteContact.fulfilled, (state, action) => {
      state.contacts = state.contacts.filter((contact) => contact.id !== action.payload);
      if (state.currentContact && state.currentContact.id === action.payload) {
        state.currentContact = null;
      }
    });

    // Leads
    builder.addCase(fetchLeads.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchLeads.fulfilled, (state, action) => {
      state.isLoading = false;
      state.leads = action.payload.results || action.payload;
    });
    builder.addCase(fetchLeads.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchLead.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchLead.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentLead = action.payload;
    });
    builder.addCase(fetchLead.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(createLead.fulfilled, (state, action) => {
      state.leads.push(action.payload);
    });

    builder.addCase(updateLead.fulfilled, (state, action) => {
      const index = state.leads.findIndex((lead) => lead.id === action.payload.id);
      if (index !== -1) {
        state.leads[index] = action.payload;
      }
      state.currentLead = action.payload;
    });

    builder.addCase(deleteLead.fulfilled, (state, action) => {
      state.leads = state.leads.filter((lead) => lead.id !== action.payload);
      if (state.currentLead && state.currentLead.id === action.payload) {
        state.currentLead = null;
      }
    });

    // Opportunities
    builder.addCase(fetchOpportunities.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchOpportunities.fulfilled, (state, action) => {
      state.isLoading = false;
      state.opportunities = action.payload.results || action.payload;
    });
    builder.addCase(fetchOpportunities.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(fetchOpportunity.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchOpportunity.fulfilled, (state, action) => {
      state.isLoading = false;
      state.currentOpportunity = action.payload;
    });
    builder.addCase(fetchOpportunity.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });

    builder.addCase(createOpportunity.fulfilled, (state, action) => {
      state.opportunities.push(action.payload);
    });

    builder.addCase(updateOpportunity.fulfilled, (state, action) => {
      const index = state.opportunities.findIndex((opportunity) => opportunity.id === action.payload.id);
      if (index !== -1) {
        state.opportunities[index] = action.payload;
      }
      state.currentOpportunity = action.payload;
    });

    builder.addCase(deleteOpportunity.fulfilled, (state, action) => {
      state.opportunities = state.opportunities.filter((opportunity) => opportunity.id !== action.payload);
      if (state.currentOpportunity && state.currentOpportunity.id === action.payload) {
        state.currentOpportunity = null;
      }
    });

    // Stats
    builder.addCase(fetchCrmStats.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(fetchCrmStats.fulfilled, (state, action) => {
      state.isLoading = false;
      state.stats = action.payload;
    });
    builder.addCase(fetchCrmStats.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload as string;
    });
  },
});

export const { clearError, clearCurrentContact, clearCurrentLead, clearCurrentOpportunity } = crmSlice.actions;
export default crmSlice.reducer;
