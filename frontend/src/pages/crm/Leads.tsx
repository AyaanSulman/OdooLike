import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  Tooltip,
  Chip,
  Typography,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { fetchLeads, deleteLead, convertLeadToOpportunity } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';

const Leads: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { leads, isLoading } = useSelector((state: RootState) => state.crm);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [convertDialogOpen, setConvertDialogOpen] = useState(false);
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchLeads());
  }, [dispatch]);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage: number) => {
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const handleAddLead = () => {
    navigate('/crm/leads/new');
  };

  const handleEditLead = (lead: any) => {
    navigate(`/crm/leads/${lead.id}`);
  };

  const handleViewLead = (lead: any) => {
    navigate(`/crm/leads/${lead.id}/view`);
  };

  const handleDeleteClick = (ids: string[]) => {
    setSelectedIds(ids);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    await Promise.all(selectedIds.map((id) => dispatch(deleteLead(id))));
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  const handleConvertClick = (id: string) => {
    setSelectedLeadId(id);
    setConvertDialogOpen(true);
  };

  const handleConvertConfirm = async () => {
    if (selectedLeadId) {
      await dispatch(convertLeadToOpportunity(selectedLeadId));
      setConvertDialogOpen(false);
      setSelectedLeadId(null);
    }
  };

  const handleConvertCancel = () => {
    setConvertDialogOpen(false);
    setSelectedLeadId(null);
  };

  // Mock data for demonstration
  const mockLeads = [
    {
      id: '1',
      first_name: 'Michael',
      last_name: 'Johnson',
      company: 'Global Tech',
      email: 'michael.johnson@globaltech.com',
      phone: '+1 (555) 123-7890',
      source: 'Website',
      status: 'New',
      created_at: '2023-06-15',
      estimated_value: 5000,
    },
    {
      id: '2',
      first_name: 'Sarah',
      last_name: 'Williams',
      company: 'Innovative Solutions',
      email: 'sarah.williams@innovative.com',
      phone: '+1 (555) 456-7890',
      source: 'Referral',
      status: 'Contacted',
      created_at: '2023-06-10',
      estimated_value: 7500,
    },
    {
      id: '3',
      first_name: 'David',
      last_name: 'Brown',
      company: 'Brown Enterprises',
      email: 'david.brown@brownent.com',
      phone: '+1 (555) 789-0123',
      source: 'Trade Show',
      status: 'Qualified',
      created_at: '2023-06-05',
      estimated_value: 10000,
    },
    {
      id: '4',
      first_name: 'Lisa',
      last_name: 'Garcia',
      company: 'Garcia & Associates',
      email: 'lisa.garcia@garcia.com',
      phone: '+1 (555) 234-5678',
      source: 'Email Campaign',
      status: 'Negotiation',
      created_at: '2023-06-01',
      estimated_value: 15000,
    },
    {
      id: '5',
      first_name: 'Robert',
      last_name: 'Martinez',
      company: 'Martinez Group',
      email: 'robert.martinez@martinezgroup.com',
      phone: '+1 (555) 876-5432',
      source: 'Social Media',
      status: 'Unqualified',
      created_at: '2023-05-25',
      estimated_value: 3000,
    },
  ];

  const leadData = leads?.length > 0 ? leads : mockLeads;

  const columns = [
    {
      id: 'name',
      label: 'Name',
      minWidth: 180,
      format: (value: string, row: any) => `${row.first_name} ${row.last_name}`,
    },
    { id: 'company', label: 'Company', minWidth: 150 },
    { id: 'email', label: 'Email', minWidth: 200 },
    { id: 'phone', label: 'Phone', minWidth: 150 },
    { id: 'source', label: 'Source', minWidth: 120 },
    {
      id: 'status',
      label: 'Status',
      minWidth: 120,
      format: (value: string) => {
        let color;
        switch (value) {
          case 'New':
            color = 'info';
            break;
          case 'Contacted':
            color = 'primary';
            break;
          case 'Qualified':
            color = 'success';
            break;
          case 'Negotiation':
            color = 'warning';
            break;
          case 'Unqualified':
            color = 'error';
            break;
          default:
            color = 'default';
        }
        return <Chip label={value} color={color as any} size="small" variant="outlined" />;
      },
    },
    {
      id: 'estimated_value',
      label: 'Est. Value',
      minWidth: 120,
      align: 'right' as const,
      format: (value: number) => `$${value.toLocaleString()}`,
    },
    { id: 'created_at', label: 'Created Date', minWidth: 120 },
  ];

  const ActionColumn = ({ row }: { row: any }) => (
    <Box sx={{ display: 'flex', gap: 1 }}>
      <Tooltip title="Convert to Opportunity">
        <Button
          size="small"
          variant="outlined"
          color="primary"
          onClick={(e) => {
            e.stopPropagation();
            handleConvertClick(row.id);
          }}
        >
          Convert
        </Button>
      </Tooltip>
    </Box>
  );

  return (
    <Box>
      <PageHeader
        title="Leads"
        subtitle="Manage your sales leads"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM' },
          { label: 'Leads' },
        ]}
        action={{
          label: 'Add Lead',
          onClick: handleAddLead,
          icon: <AddIcon />,
        }}
      />

      <DataTable
        columns={columns}
        rows={leadData}
        title="Leads"
        onEdit={handleEditLead}
        onDelete={handleDeleteClick}
        onView={handleViewLead}
        selectable={true}
        loading={isLoading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        totalCount={leadData.length}
        renderCustomActions={({ row }) => <ActionColumn row={row} />}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete {selectedIds.length > 1 ? 'these leads' : 'this lead'}?
            This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} color="primary">
            Cancel
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" autoFocus>
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Convert Lead Dialog */}
      <Dialog
        open={convertDialogOpen}
        onClose={handleConvertCancel}
        aria-labelledby="convert-dialog-title"
        aria-describedby="convert-dialog-description"
      >
        <DialogTitle id="convert-dialog-title">Convert Lead to Opportunity</DialogTitle>
        <DialogContent>
          <DialogContentText id="convert-dialog-description">
            Are you sure you want to convert this lead to an opportunity? This will move the lead to your sales pipeline.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleConvertCancel} color="primary">
            Cancel
          </Button>
          <Button onClick={handleConvertConfirm} color="primary" variant="contained" autoFocus>
            Convert
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Leads;
