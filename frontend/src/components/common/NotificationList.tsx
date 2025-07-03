import React, { useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Typography,
  Divider,
  Box,
  Button,
  Popover,
} from '@mui/material';
import {
  ShoppingCart as ShoppingCartIcon,
  Person as PersonIcon,
  Assignment as AssignmentIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';

const notifications = [
  {
    id: 1,
    type: 'order',
    message: 'New purchase order #PO-2023-001 has been created',
    time: '5 minutes ago',
  },
  {
    id: 2,
    type: 'stock',
    message: 'Product "Laptop XPS 15" is running low on stock',
    time: '1 hour ago',
  },
  {
    id: 3,
    type: 'lead',
    message: 'New lead assigned: John Smith from Acme Corp',
    time: '3 hours ago',
  },
  {
    id: 4,
    type: 'alert',
    message: 'System maintenance scheduled for tonight at 2 AM',
    time: 'Yesterday',
  },
];

const getNotificationIcon = (type: string) => {
  switch (type) {
    case 'order':
      return <ShoppingCartIcon />;
    case 'stock':
      return <WarningIcon />;
    case 'lead':
      return <PersonIcon />;
    case 'alert':
    default:
      return <AssignmentIcon />;
  }
};

const getAvatarColorByType = (type: string) => {
  switch (type) {
    case 'order':
      return 'primary.main';
    case 'lead':
      return 'success.main';
    case 'stock':
      return 'warning.main';
    case 'alert':
      return 'error.main';
    default:
      return 'grey.500';
  }
};

interface NotificationListProps {
  open: boolean;
  onClose: () => void;
  anchorEl: HTMLElement | null;
}

const NotificationList: React.FC<NotificationListProps> = ({ open, onClose, anchorEl }) => {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'order',
      message: 'New purchase order #PO-2023-001 has been created',
      time: '5 minutes ago',
    },
    {
      id: 2,
      type: 'stock',
      message: 'Product "Laptop XPS 15" is running low on stock',
      time: '1 hour ago',
    },
    {
      id: 3,
      type: 'lead',
      message: 'New lead assigned: John Smith from Acme Corp',
      time: '3 hours ago',
    },
    {
      id: 4,
      type: 'alert',
      message: 'System maintenance scheduled for tonight at 2 AM',
      time: 'Yesterday',
    },
  ]);

  return (
    <Popover
      open={open}
      anchorEl={anchorEl}
      onClose={onClose}
      anchorOrigin={{
        vertical: 'bottom',
        horizontal: 'right',
      }}
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      PaperProps={{
        style: { width: 350, maxHeight: 500, overflow: 'auto' },
      }}
    >
      <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">Notifications</Typography>
        <Button size="small">Mark all as read</Button>
      </Box>
      <Divider />
      {notifications.length > 0 ? (
        <List sx={{ width: '100%', bgcolor: 'background.paper', p: 0 }}>
          {notifications.map((notification, index) => (
            <React.Fragment key={notification.id}>
              <ListItem alignItems="flex-start" sx={{ px: 2, py: 1.5 }}>
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: getAvatarColorByType(notification.type) }}>
                    {getNotificationIcon(notification.type)}
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={notification.message}
                  secondary={
                    <Typography
                      sx={{ display: 'block' }}
                      component="span"
                      variant="body2"
                      color="text.secondary"
                    >
                      {notification.time}
                    </Typography>
                  }
                />
              </ListItem>
              {index < notifications.length - 1 && <Divider variant="inset" component="li" />}
            </React.Fragment>
          ))}
        </List>
      ) : (
        <Box sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="textSecondary">No notifications</Typography>
        </Box>
      )}
      <Divider />
      <Box sx={{ p: 1.5, textAlign: 'center' }}>
        <Button size="small" fullWidth>
          View all notifications
        </Button>
      </Box>
    </Popover>
  );
};

export default NotificationList;
