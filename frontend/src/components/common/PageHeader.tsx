import React from 'react';
import { Box, Typography, Breadcrumbs, Button, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  breadcrumbs?: Array<{
    label: string;
    path?: string;
  }>;
  action?: {
    label: string;
    onClick: () => void;
    icon?: React.ReactNode;
  };
}

const PageHeader: React.FC<PageHeaderProps> = ({ title, subtitle, breadcrumbs, action }) => {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        mb: 3,
        borderRadius: 2,
        backgroundColor: 'background.paper',
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          {breadcrumbs && breadcrumbs.length > 0 && (
            <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 1 }}>
              {breadcrumbs.map((crumb, index) => {
                const isLast = index === breadcrumbs.length - 1;
                return isLast || !crumb.path ? (
                  <Typography
                    key={crumb.label}
                    color={isLast ? 'text.primary' : 'text.secondary'}
                    sx={{ fontWeight: isLast ? 'medium' : 'normal' }}
                  >
                    {crumb.label}
                  </Typography>
                ) : (
                  <RouterLink
                    key={crumb.label}
                    to={crumb.path}
                    style={{ color: 'inherit', textDecoration: 'none' }}
                  >
                    {crumb.label}
                  </RouterLink>
                );
              })}
            </Breadcrumbs>
          )}
          <Typography variant="h4" component="h1" gutterBottom>
            {title}
          </Typography>
          {subtitle && (
            <Typography variant="subtitle1" color="text.secondary">
              {subtitle}
            </Typography>
          )}
        </Box>
        {action && (
          <Button
            variant="contained"
            color="primary"
            startIcon={action.icon}
            onClick={action.onClick}
          >
            {action.label}
          </Button>
        )}
      </Box>
    </Paper>
  );
};

export default PageHeader;
