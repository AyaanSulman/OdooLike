import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { styled } from '@mui/material/styles';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Tooltip,
  Badge,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  Person as PersonIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../../store';
import { logout } from '../../store/slices/authSlice';
import { toggleSidebar, toggleDarkMode } from '../../store/slices/uiSlice';
import { AppDispatch } from '../../store';
import NotificationList from '../common/NotificationList';
import Sidebar from '../navigation/Sidebar';

const drawerWidth = 280;

const Main = styled('main')(
  ({ theme }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    marginLeft: 0,
    [theme.breakpoints.up('md')]: {
      marginLeft: drawerWidth,
    },
  })
);

const MainLayout: React.FC = () => {
  const theme = useTheme();
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Redux state
  const { user } = useSelector((state: RootState) => state.auth);
  const { sidebarOpen, darkMode } = useSelector((state: RootState) => state.ui);
  
  // Local state
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);
  const [anchorElNotifications, setAnchorElNotifications] = useState<null | HTMLElement>(null);
  const [notificationOpen, setNotificationOpen] = useState(false);

  const handleDrawerToggle = () => {
    dispatch(toggleSidebar());
  };

  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setAnchorElUser(null);
  };

  const handleNotificationOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNotifications(event.currentTarget);
    setNotificationOpen(true);
  };

  const handleNotificationClose = () => {
    setAnchorElNotifications(null);
    setNotificationOpen(false);
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate('/auth/login');
    handleUserMenuClose();
  };

  const handleToggleDarkMode = () => {
    dispatch(toggleDarkMode());
  };

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            OdooLike ERP
          </Typography>
          
          {/* Dark Mode Toggle */}
          <Tooltip title={darkMode ? 'Light Mode' : 'Dark Mode'}>
            <IconButton color="inherit" onClick={handleToggleDarkMode}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Tooltip>
          
          {/* Notifications */}
          <Tooltip title="Notifications">
            <IconButton color="inherit" onClick={handleNotificationOpen}>
              <Badge badgeContent={4} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>
          
          {/* Settings */}
          <Tooltip title="Settings">
            <IconButton color="inherit">
              <SettingsIcon />
            </IconButton>
          </Tooltip>
          
          {/* User Menu */}
          <Tooltip title="Account settings">
            <IconButton onClick={handleUserMenuOpen} sx={{ p: 0, ml: 2 }}>
              <Avatar alt={user?.first_name || 'User'} src="/static/images/avatar/2.jpg" />
            </IconButton>
          </Tooltip>
          
          <Menu
            sx={{ mt: '45px' }}
            id="menu-appbar"
            anchorEl={anchorElUser}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorElUser)}
            onClose={handleUserMenuClose}
          >
            <MenuItem onClick={handleUserMenuClose}>
              <PersonIcon sx={{ mr: 1 }} />
              Profile
            </MenuItem>
            <MenuItem onClick={handleUserMenuClose}>
              <SettingsIcon sx={{ mr: 1 }} />
              Settings
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <LogoutIcon sx={{ mr: 1 }} />
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>
      
      {/* Sidebar Navigation */}
      <Sidebar
        open={sidebarOpen}
        onClose={handleDrawerToggle}
        drawerWidth={drawerWidth}
      />
      
      {/* Main Content */}
      <Main>
        <Toolbar /> {/* This creates space for the fixed AppBar */}
        <Outlet />
      </Main>
      
      {/* Notifications Panel */}
      <NotificationList
        open={notificationOpen}
        onClose={handleNotificationClose}
        anchorEl={anchorElNotifications}
      />
    </Box>
  );
};

export default MainLayout;
