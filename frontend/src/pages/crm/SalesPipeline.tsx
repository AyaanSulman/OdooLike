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
  Typography,
  Card,
  CardContent,
  CardActions,
  Grid,
  Paper,
  Chip,
  IconButton,
  Tooltip,
  Divider,
  Stack,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Visibility as VisibilityIcon,
  ArrowForward as ArrowForwardIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { fetchOpportunities, deleteOpportunity, updateOpportunityStage } from '../../store/slices/crmSlice';
import { RootState } from '../../store';
import { AppDispatch } from '../../store';
import PageHeader from '../../components/common/PageHeader';

interface Opportunity {
  id: string;
  name: string;
  contact_name: string;
  company: string;
  stage: string;
  amount: number;
  close_date: string;
  probability: number;
  created_at: string;
  description?: string;
}

const SalesPipeline: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { opportunities, isLoading } = useSelector((state: RootState) => state.crm);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchOpportunities());
  }, [dispatch]);

  const handleAddOpportunity = () => {
    navigate('/crm/opportunities/new');
  };

  const handleEditOpportunity = (id: string) => {
    navigate(`/crm/opportunities/${id}`);
  };

  const handleViewOpportunity = (id: string) => {
    navigate(`/crm/opportunities/${id}/view`);
  };

  const handleDeleteClick = (id: string) => {
    setSelectedId(id);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (selectedId) {
      await dispatch(deleteOpportunity(selectedId));
      setDeleteDialogOpen(false);
      setSelectedId(null);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setSelectedId(null);
  };

  const handleMoveStage = async (id: string, currentStage: string, direction: 'forward' | 'back') => {
    const stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'];
    const currentIndex = stages.indexOf(currentStage);
    let newIndex;

    if (direction === 'forward' && currentIndex < stages.length - 1) {
      newIndex = currentIndex + 1;
    } else if (direction === 'back' && currentIndex > 0) {
      newIndex = currentIndex - 1;
    } else {
      return; // Can't move further
    }

    await dispatch(updateOpportunityStage({ id, stage: stages[newIndex] }));
  };

  // Mock data for demonstration
  const mockOpportunities: Opportunity[] = [
    {
      id: '1',
      name: 'Enterprise Software License',
      contact_name: 'John Smith',
      company: 'Acme Corp',
      stage: 'Prospecting',
      amount: 25000,
      close_date: '2023-08-15',
      probability: 20,
      created_at: '2023-06-01',
      description: 'Potential enterprise license deal for 100 users',
    },
    {
      id: '2',
      name: 'Cloud Migration Project',
      contact_name: 'Sarah Williams',
      company: 'Innovative Solutions',
      stage: 'Qualification',
      amount: 45000,
      close_date: '2023-07-30',
      probability: 40,
      created_at: '2023-05-20',
      description: 'Migration from on-prem to cloud infrastructure',
    },
    {
      id: '3',
      name: 'Annual Support Contract',
      contact_name: 'Robert Johnson',
      company: 'Tech Solutions',
      stage: 'Proposal',
      amount: 12000,
      close_date: '2023-07-10',
      probability: 60,
      created_at: '2023-05-15',
      description: 'Annual support and maintenance renewal',
    },
    {
      id: '4',
      name: 'Hardware Upgrade',
      contact_name: 'Emily Williams',
      company: 'Global Services',
      stage: 'Negotiation',
      amount: 75000,
      close_date: '2023-06-30',
      probability: 80,
      created_at: '2023-04-10',
      description: 'Complete hardware refresh for main office',
    },
    {
      id: '5',
      name: 'Software Implementation',
      contact_name: 'Michael Brown',
      company: 'Brown Enterprises',
      stage: 'Closed Won',
      amount: 35000,
      close_date: '2023-05-15',
      probability: 100,
      created_at: '2023-03-01',
      description: 'ERP software implementation project',
    },
    {
      id: '6',
      name: 'Consulting Services',
      contact_name: 'Lisa Garcia',
      company: 'Garcia & Associates',
      stage: 'Closed Lost',
      amount: 20000,
      close_date: '2023-05-01',
      probability: 0,
      created_at: '2023-02-15',
      description: 'Strategic consulting services proposal',
    },
  ];

  const opportunityData = opportunities?.length > 0 ? opportunities : mockOpportunities;

  // Group opportunities by stage
  const stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'];
  const opportunitiesByStage = stages.reduce<Record<string, Opportunity[]>>((acc, stage) => {
    acc[stage] = opportunityData.filter((opp) => opp.stage === stage);
    return acc;
  }, {});

  // Calculate stage totals
  const stageTotals = stages.reduce<Record<string, { count: number; value: number }>>((acc, stage) => {
    const opps = opportunitiesByStage[stage] || [];
    acc[stage] = {
      count: opps.length,
      value: opps.reduce((sum, opp) => sum + opp.amount, 0),
    };
    return acc;
  }, {});

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'Prospecting':
        return '#e3f2fd'; // light blue
      case 'Qualification':
        return '#e8f5e9'; // light green
      case 'Proposal':
        return '#fffde7'; // light yellow
      case 'Negotiation':
        return '#fff3e0'; // light orange
      case 'Closed Won':
        return '#e8f5e9'; // light green
      case 'Closed Lost':
        return '#ffebee'; // light red
      default:
        return '#f5f5f5'; // light grey
    }
  };

  const getChipColor = (stage: string): 'default' | 'primary' | 'secondary' | 'error' | 'info' | 'success' | 'warning' => {
    switch (stage) {
      case 'Prospecting':
        return 'info';
      case 'Qualification':
        return 'primary';
      case 'Proposal':
        return 'secondary';
      case 'Negotiation':
        return 'warning';
      case 'Closed Won':
        return 'success';
      case 'Closed Lost':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <PageHeader
        title="Sales Pipeline"
        subtitle="Manage your sales opportunities"
        breadcrumbs={[
          { label: 'Dashboard', path: '/' },
          { label: 'CRM' },
          { label: 'Sales Pipeline' },
        ]}
        action={{
          label: 'Add Opportunity',
          onClick: handleAddOpportunity,
          icon: <AddIcon />,
        }}
      />

      <Box sx={{ overflowX: 'auto', pb: 2 }}>
        <Grid container spacing={2} sx={{ minWidth: stages.length * 300 }}>
          {stages.map((stage) => (
            <Grid item xs={12 / stages.length} key={stage}>
              <Paper
                sx={{
                  height: '100%',
                  backgroundColor: getStageColor(stage),
                  borderRadius: 1,
                  overflow: 'hidden',
                }}
                elevation={1}
              >
                <Box
                  sx={{
                    p: 2,
                    backgroundColor: 'rgba(0,0,0,0.03)',
                    borderBottom: '1px solid rgba(0,0,0,0.1)',
                  }}
                >
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography variant="h6" component="div">
                        {stage}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {stageTotals[stage]?.count || 0} deals • $
                        {(stageTotals[stage]?.value || 0).toLocaleString()}
                      </Typography>
                    </Box>
                    <Chip
                      label={`${stageTotals[stage]?.count || 0}`}
                      color={getChipColor(stage)}
                      size="small"
                      variant="outlined"
                    />
                  </Stack>
                </Box>
                <Box sx={{ p: 1, maxHeight: 'calc(100vh - 250px)', overflowY: 'auto' }}>
                  {opportunitiesByStage[stage]?.map((opportunity) => (
                    <Card
                      key={opportunity.id}
                      sx={{
                        mb: 1,
                        '&:hover': {
                          boxShadow: 3,
                        },
                      }}
                      variant="outlined"
                    >
                      <CardContent sx={{ pb: 1 }}>
                        <Typography variant="subtitle1" component="div" noWrap>
                          {opportunity.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" noWrap>
                          {opportunity.company}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {opportunity.contact_name}
                        </Typography>
                        <Box sx={{ mt: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="h6" component="div" color="primary">
                            ${opportunity.amount.toLocaleString()}
                          </Typography>
                          <Chip
                            label={`${opportunity.probability}%`}
                            size="small"
                            color={
                              opportunity.probability >= 70
                                ? 'success'
                                : opportunity.probability >= 30
                                ? 'warning'
                                : 'error'
                            }
                          />
                        </Box>
                        <Typography variant="caption" display="block" color="text.secondary">
                          Close: {opportunity.close_date}
                        </Typography>
                      </CardContent>
                      <Divider />
                      <CardActions sx={{ justifyContent: 'space-between', py: 0.5 }}>
                        <Box>
                          <Tooltip title="View">
                            <IconButton
                              size="small"
                              onClick={() => handleViewOpportunity(opportunity.id)}
                              color="primary"
                            >
                              <VisibilityIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Edit">
                            <IconButton
                              size="small"
                              onClick={() => handleEditOpportunity(opportunity.id)}
                              color="primary"
                            >
                              <EditIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Delete">
                            <IconButton
                              size="small"
                              onClick={() => handleDeleteClick(opportunity.id)}
                              color="error"
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Box>
                        <Box>
                          {stage !== 'Prospecting' && (
                            <Tooltip title="Move Back">
                              <IconButton
                                size="small"
                                onClick={() => handleMoveStage(opportunity.id, stage, 'back')}
                              >
                                <ArrowBackIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          )}
                          {stage !== 'Closed Won' && stage !== 'Closed Lost' && (
                            <Tooltip title="Move Forward">
                              <IconButton
                                size="small"
                                onClick={() => handleMoveStage(opportunity.id, stage, 'forward')}
                              >
                                <ArrowForwardIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          )}
                        </Box>
                      </CardActions>
                    </Card>
                  ))}
                  {(!opportunitiesByStage[stage] || opportunitiesByStage[stage].length === 0) && (
                    <Box sx={{ p: 2, textAlign: 'center' }}>
                      <Typography variant="body2" color="text.secondary">
                        No opportunities in this stage
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Box>

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
            Are you sure you want to delete this opportunity? This action cannot be undone.
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

export default SalesPipeline;
