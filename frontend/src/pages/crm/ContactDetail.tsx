import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Box, Alert } from '@mui/material';
import { fetchContactById, createContact, updateContact } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import FormikForm, { FormField } from '../../components/common/FormikForm';

const ContactDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isNewContact = id === 'new';
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { contact, isLoading, error } = useSelector((state: RootState) => state.crm);
  const [initialValues, setInitialValues] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    company: '',
    job_title: '',
    type: '',
    status: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
    website: '',
    notes: '',
    is_active: true,
  });

  useEffect(() => {
    if (!isNewContact && id) {
      dispatch(fetchContactById(id));
    }
  }, [dispatch, id, isNewContact]);

  useEffect(() => {
    if (!isNewContact && contact) {
      setInitialValues({
        first_name: contact.first_name || '',
        last_name: contact.last_name || '',
        email: contact.email || '',
        phone: contact.phone || '',
        company: contact.company || '',
        job_title: contact.job_title || '',
        type: contact.type || '',
        status: contact.status || '',
        address: contact.address || '',
        city: contact.city || '',
        state: contact.state || '',
        zip_code: contact.zip_code || '',
        country: contact.country || '',
        website: contact.website || '',
        notes: contact.notes || '',
        is_active: contact.is_active !== false,
      });
    }
  }, [contact, isNewContact]);

  const validationSchema = Yup.object({
    first_name: Yup.string().required('First name is required'),
    last_name: Yup.string().required('Last name is required'),
    email: Yup.string().email('Enter a valid email').required('Email is required'),
    phone: Yup.string(),
    company: Yup.string(),
    type: Yup.string().required('Contact type is required'),
    status: Yup.string().required('Status is required'),
  });

  const handleSubmit = async (values: any) => {
    if (isNewContact) {
      await dispatch(createContact(values));
    } else if (id) {
      await dispatch(updateContact({ id, ...values }));
    }

    navigate('/crm/contacts');
  };

  const handleCancel = () => {
    navigate('/crm/contacts');
  };

  const typeOptions = [
    { value: 'Customer', label: 'Customer' },
    { value: 'Lead', label: 'Lead' },
    { value: 'Supplier', label: 'Supplier' },
    { value: 'Partner', label: 'Partner' },
    { value: 'Other', label: 'Other' },
  ];

  const statusOptions = [
    { value: 'Active', label: 'Active' },
    { value: 'Inactive', label: 'Inactive' },
    { value: 'New', label: 'New' },
    { value: 'Qualified', label: 'Qualified' },
    { value: 'Unqualified', label: 'Unqualified' },
  ];

  const formSections = [
    {
      title: 'Basic Information',
      fields: [
        {
          name: 'first_name',
          label: 'First Name',
          type: 'text',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'last_name',
          label: 'Last Name',
          type: 'text',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'email',
          label: 'Email',
          type: 'email',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'phone',
          label: 'Phone',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'company',
          label: 'Company',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'job_title',
          label: 'Job Title',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'type',
          label: 'Contact Type',
          type: 'select',
          options: typeOptions,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'status',
          label: 'Status',
          type: 'select',
          options: statusOptions,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
      ],
    },
    {
      title: 'Address Information',
      fields: [
        {
          name: 'address',
          label: 'Address',
          type: 'text',
          gridProps: { xs: 12 },
        },
        {
          name: 'city',
          label: 'City',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'state',
          label: 'State/Province',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'zip_code',
          label: 'ZIP/Postal Code',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'country',
          label: 'Country',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'website',
          label: 'Website',
          type: 'text',
          gridProps: { xs: 12 },
        },
      ],
    },
    {
      title: 'Additional Information',
      fields: [
        {
          name: 'notes',
          label: 'Notes',
          type: 'textarea',
          multiline: true,
          rows: 4,
          gridProps: { xs: 12 },
        },
        {
          name: 'is_active',
          label: 'Active Contact',
          type: 'checkbox',
          gridProps: { xs: 12 },
        },
      ],
    },
  ];

  return (
    <Box>
      <PageHeader
        title={isNewContact ? 'Add New Contact' : 'Edit Contact'}
        subtitle={isNewContact ? 'Create a new contact in your CRM' : 'Update contact details'}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM', path: '/crm' },
          { label: 'Contacts', path: '/crm/contacts' },
          { label: isNewContact ? 'Add New' : 'Edit' },
        ]}
      />

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <FormikForm
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        sections={formSections}
        submitButtonText={isNewContact ? 'Create Contact' : 'Update Contact'}
        cancelButtonText="Cancel"
        onCancel={handleCancel}
        loading={isLoading}
        error={error}
      />
    </Box>
  );
};

export default ContactDetail;
