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
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { fetchContacts, deleteContact } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';

const Contacts: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { contacts, isLoading } = useSelector((state: RootState) => state.crm);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  useEffect(() => {
    dispatch(fetchContacts());
  }, [dispatch]);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage: number) => {
    setRowsPerPage(newRowsPerPage);
    setPage(0);
  };

  const handleAddContact = () => {
    navigate('/crm/contacts/new');
  };

  const handleEditContact = (contact: any) => {
    navigate(`/crm/contacts/${contact.id}`);
  };

  const handleViewContact = (contact: any) => {
    navigate(`/crm/contacts/${contact.id}/view`);
  };

  const handleDeleteClick = (ids: string[]) => {
    setSelectedIds(ids);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    await Promise.all(selectedIds.map((id) => dispatch(deleteContact(id))));
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setSelectedIds([]);
  };

  // Mock data for demonstration
  const mockContacts = [
    {
      id: '1',
      first_name: 'John',
      last_name: 'Smith',
      company: 'Acme Corp',
      email: 'john.smith@acme.com',
      phone: '+1 (555) 123-4567',
      type: 'Customer',
      status: 'Active',
      created_at: '2023-05-15',
    },
    {
      id: '2',
      first_name: 'Jane',
      last_name: 'Doe',
      company: 'XYZ Industries',
      email: 'jane.doe@xyz.com',
      phone: '+1 (555) 987-6543',
      type: 'Lead',
      status: 'New',
      created_at: '2023-06-02',
    },
    {
      id: '3',
      first_name: 'Robert',
      last_name: 'Johnson',
      company: 'Tech Solutions',
      email: 'robert.johnson@techsolutions.com',
      phone: '+1 (555) 456-7890',
      type: 'Supplier',
      status: 'Active',
      created_at: '2023-04-10',
    },
    {
      id: '4',
      first_name: 'Emily',
      last_name: 'Williams',
      company: 'Global Services',
      email: 'emily.williams@globalservices.com',
      phone: '+1 (555) 234-5678',
      type: 'Customer',
      status: 'Inactive',
      created_at: '2023-03-22',
    },
    {
      id: '5',
      first_name: 'Michael',
      last_name: 'Brown',
      company: 'Brown Enterprises',
      email: 'michael.brown@brownent.com',
      phone: '+1 (555) 876-5432',
      type: 'Lead',
      status: 'Qualified',
      created_at: '2023-06-10',
    },
  ];

  const contactData = contacts?.length > 0 ? contacts : mockContacts;

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
    {
      id: 'type',
      label: 'Type',
      minWidth: 120,
      format: (value: string) => {
        let color;
        switch (value) {
          case 'Customer':
            color = 'primary';
            break;
          case 'Lead':
            color = 'secondary';
            break;
          case 'Supplier':
            color = 'success';
            break;
          default:
            color = 'default';
        }
        return <Chip label={value} color={color as any} size="small" />;
      },
    },
    {
      id: 'status',
      label: 'Status',
      minWidth: 120,
      format: (value: string) => {
        let color;
        switch (value) {
          case 'Active':
            color = 'success';
            break;
          case 'Inactive':
            color = 'error';
            break;
          case 'New':
            color = 'info';
            break;
          case 'Qualified':
            color = 'warning';
            break;
          default:
            color = 'default';
        }
        return <Chip label={value} color={color as any} size="small" variant="outlined" />;
      },
    },
    { id: 'created_at', label: 'Created Date', minWidth: 120 },
  ];

  return (
    <Box>
      <PageHeader
        title="Contacts"
        subtitle="Manage your contacts, leads, and customers"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM' },
          { label: 'Contacts' },
        ]}
        action={{
          label: 'Add Contact',
          onClick: handleAddContact,
          icon: <AddIcon />,
        }}
      />

      <DataTable
        columns={columns}
        rows={contactData}
        title="Contacts"
        onEdit={handleEditContact}
        onDelete={handleDeleteClick}
        onView={handleViewContact}
        selectable={true}
        loading={isLoading}
        page={page}
        rowsPerPage={rowsPerPage}
        onPageChange={handlePageChange}
        onRowsPerPageChange={handleRowsPerPageChange}
        totalCount={contactData.length}
      />

      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete {selectedIds.length > 1 ? 'these contacts' : 'this contact'}?
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
    </Box>
  );
};

export default Contacts;
