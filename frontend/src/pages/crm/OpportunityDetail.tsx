import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import * as Yup from 'yup';
import { Box, Alert } from '@mui/material';
import { fetchOpportunityById, createOpportunity, updateOpportunity } from '../../store/slices/crmSlice';
import { fetchContacts } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';
import FormikForm, { FormField } from '../../components/common/FormikForm';

const OpportunityDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isNewOpportunity = id === 'new';
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { opportunity, contacts, isLoading, error } = useSelector((state: RootState) => state.crm);
  const [initialValues, setInitialValues] = useState({
    name: '',
    contact_id: '',
    company: '',
    stage: 'Prospecting',
    amount: 0,
    close_date: '',
    probability: 20,
    description: '',
    source: '',
    expected_revenue: 0,
    next_step: '',
    assigned_to: '',
  });

  useEffect(() => {
    dispatch(fetchContacts());
    if (!isNewOpportunity && id) {
      dispatch(fetchOpportunityById(id));
    }
  }, [dispatch, id, isNewOpportunity]);

  useEffect(() => {
    if (!isNewOpportunity && opportunity) {
      setInitialValues({
        name: opportunity.name || '',
        contact_id: opportunity.contact_id || '',
        company: opportunity.company || '',
        stage: opportunity.stage || 'Prospecting',
        amount: opportunity.amount || 0,
        close_date: opportunity.close_date || '',
        probability: opportunity.probability || 20,
        description: opportunity.description || '',
        source: opportunity.source || '',
        expected_revenue: opportunity.expected_revenue || 0,
        next_step: opportunity.next_step || '',
        assigned_to: opportunity.assigned_to || '',
      });
    }
  }, [opportunity, isNewOpportunity]);

  const validationSchema = Yup.object({
    name: Yup.string().required('Opportunity name is required'),
    contact_id: Yup.string().required('Contact is required'),
    company: Yup.string().required('Company is required'),
    stage: Yup.string().required('Stage is required'),
    amount: Yup.number().min(0, 'Amount must be positive').required('Amount is required'),
    close_date: Yup.date().required('Close date is required'),
    probability: Yup.number().min(0, 'Probability must be between 0 and 100').max(100, 'Probability must be between 0 and 100'),
  });

  const handleSubmit = async (values: any) => {
    // Calculate expected revenue based on amount and probability
    const calculatedValues = {
      ...values,
      expected_revenue: (values.amount * values.probability) / 100,
    };

    if (isNewOpportunity) {
      await dispatch(createOpportunity(calculatedValues));
    } else if (id) {
      await dispatch(updateOpportunity({ id, ...calculatedValues }));
    }

    navigate('/crm/pipeline');
  };

  const handleCancel = () => {
    navigate('/crm/pipeline');
  };

  // Mock contacts data for demonstration
  const mockContactsData = [
    { id: '1', name: 'John Smith', company: 'Acme Corp' },
    { id: '2', name: 'Jane Doe', company: 'XYZ Industries' },
    { id: '3', name: 'Robert Johnson', company: 'Tech Solutions' },
    { id: '4', name: 'Emily Williams', company: 'Global Services' },
    { id: '5', name: 'Michael Brown', company: 'Brown Enterprises' },
  ];

  const contactsData = contacts?.length > 0 ? contacts : mockContactsData;

  const stageOptions = [
    { value: 'Prospecting', label: 'Prospecting' },
    { value: 'Qualification', label: 'Qualification' },
    { value: 'Proposal', label: 'Proposal' },
    { value: 'Negotiation', label: 'Negotiation' },
    { value: 'Closed Won', label: 'Closed Won' },
    { value: 'Closed Lost', label: 'Closed Lost' },
  ];

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

  const formSections = [
    {
      title: 'Opportunity Information',
      fields: [
        {
          name: 'name',
          label: 'Opportunity Name',
          type: 'text',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'contact_id',
          label: 'Contact',
          type: 'select',
          options: contactsData.map(contact => ({
            value: contact.id,
            label: `${contact.name} (${contact.company})`,
          })),
          required: true,
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
          name: 'source',
          label: 'Source',
          type: 'select',
          options: sourceOptions,
          gridProps: { xs: 12, sm: 6 },
        },
      ],
    },
    {
      title: 'Deal Information',
      fields: [
        {
          name: 'stage',
          label: 'Stage',
          type: 'select',
          options: stageOptions,
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'amount',
          label: 'Amount ($)',
          type: 'number',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'probability',
          label: 'Probability (%)',
          type: 'number',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'close_date',
          label: 'Expected Close Date',
          type: 'date',
          required: true,
          gridProps: { xs: 12, sm: 6 },
        },
      ],
    },
    {
      title: 'Additional Information',
      fields: [
        {
          name: 'next_step',
          label: 'Next Step',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'assigned_to',
          label: 'Assigned To',
          type: 'text',
          gridProps: { xs: 12, sm: 6 },
        },
        {
          name: 'description',
          label: 'Description',
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
        title={isNewOpportunity ? 'Add New Opportunity' : 'Edit Opportunity'}
        subtitle={isNewOpportunity ? 'Create a new sales opportunity' : 'Update opportunity details'}
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM', path: '/crm' },
          { label: 'Sales Pipeline', path: '/crm/pipeline' },
          { label: isNewOpportunity ? 'Add New' : 'Edit' },
        ]}
      />

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <FormikForm
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        sections={formSections}
        submitButtonText={isNewOpportunity ? 'Create Opportunity' : 'Update Opportunity'}
        cancelButtonText="Cancel"
        onCancel={handleCancel}
        loading={isLoading}
        error={error}
      />
    </Box>
  );
};

export default OpportunityDetail;
