import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Box, Alert } from '@mui/material';
import { fetchLead, createLead, updateLead } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import FormikForm, { FormField } from '../../components/common/FormikForm';

const LeadDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isNewLead = id === 'new';
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { currentLead, isLoading, error } = useSelector((state: RootState) => state.crm);
  const [initialValues, setInitialValues] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    company: '',
    job_title: '',
    source: '',
    status: 'New',
    estimated_value: 0,
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
    website: '',
    notes: '',
  });

  useEffect(() => {
    if (!isNewLead && id) {
      dispatch(fetchLead(id));
    }
  }, [dispatch, id, isNewLead]);

  useEffect(() => {
    if (!isNewLead && currentLead) {
      setInitialValues({
        first_name: currentLead.first_name || '',
        last_name: currentLead.last_name || '',
        email: currentLead.email || '',
        phone: currentLead.phone || '',
        company: currentLead.company || '',
        job_title: currentLead.job_title || '',
        source: currentLead.source || '',
        status: currentLead.status || 'New',
        estimated_value: currentLead.estimated_value || 0,
        address: currentLead.address || '',
        city: currentLead.city || '',
        state: currentLead.state || '',
        zip_code: currentLead.zip_code || '',
        country: currentLead.country || '',
        website: currentLead.website || '',
        notes: currentLead.notes || '',
      });
    }
  }, [currentLead, isNewLead]);

  const validationSchema = Yup.object({
    first_name: Yup.string().required('First name is required'),
    last_name: Yup.string().required('Last name is required'),
    email: Yup.string().email('Enter a valid email').required('Email is required'),
    company: Yup.string().required('Company is required'),
    source: Yup.string().required('Source is required'),
    status: Yup.string().required('Status is required'),
  });

  const handleSubmit = async (values: any) => {
    if (isNewLead) {
      await dispatch(createLead(values));
    } else if (id) {
      await dispatch(updateLead({ id, ...values }));
    }

    navigate('/crm/leads');
  };

  const handleCancel = () => {
    navigate('/crm/leads');
  };

  const sourceOptions = [
    { value: 'Website', label: 'Website' },
    { value: 'Referral', label: 'Referral' },
    { value: 'Trade Show', label: 'Trade Show' },
    { value: 'Email Campaign', label: 'Email Campaign' },
    { value: 'Social Media', label: 'Social Media' },
    { value: 'Cold Call', label: 'Cold Call' },
    { value: 'Partner', label: 'Partner' },
    { value: 'Other', label: 'Other' },
  ];

  const statusOptions = [
    { value: 'New', label: 'New' },
    { value: 'Contacted', label: 'Contacted' },
    { value: 'Qualified', label: 'Qualified' },
    { value: 'Negotiation', label: 'Negotiation' },
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
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'job_title',
          label: 'Job Title',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'source',
          label: 'Lead Source',
          type: 'select',
          options: sourceOptions,
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
        {
          name: 'estimated_value',
          label: 'Estimated Value ($)',
          type: 'number',
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
      ],
    },
  ];

  return (
    <Box>
      <PageHeader
        title={isNewLead ? 'Add New Lead' : 'Edit Lead'}
        subtitle={isNewLead ? 'Create a new sales lead' : 'Update lead details'}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM', path: '/crm' },
          { label: 'Leads', path: '/crm/leads' },
          { label: isNewLead ? 'Add New' : 'Edit' },
        ]}
      />

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <FormikForm
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        sections={formSections}
        submitButtonText={isNewLead ? 'Create Lead' : 'Update Lead'}
        cancelButtonText="Cancel"
        onCancel={handleCancel}
        loading={isLoading}
        error={error}
      />
    </Box>
  );
};

export default LeadDetail;
