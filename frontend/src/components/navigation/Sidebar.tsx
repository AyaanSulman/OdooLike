import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Divider,
  Typography,
  useTheme,
  useMediaQuery,
  IconButton,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Inventory as InventoryIcon,
  Category as CategoryIcon,
  Warehouse as WarehouseIcon,
  Assessment as AssessmentIcon,
  ShoppingCart as ShoppingCartIcon,
  People as PeopleIcon,
  ContactPhone as ContactPhoneIcon,
  LeaderboardOutlined as LeaderboardIcon,
  ExpandLess,
  ExpandMore,
  MenuOpen as MenuOpenIcon,
  AccountBalance as AccountBalanceIcon,
  Receipt as ReceiptIcon,
  Payments as PaymentsIcon,
  Person as PersonIcon,
  Work as WorkIcon,
  AccessTime as AccessTimeIcon,
  AttachMoney as AttachMoneyIcon,
} from '@mui/icons-material';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
  drawerWidth: number;
}

interface NavItem {
  title: string;
  path?: string;
  icon: React.ReactNode;
  children?: NavItem[];
}

const Sidebar: React.FC<SidebarProps> = ({ open, onClose, drawerWidth }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Track which menu sections are expanded
  const [openMenus, setOpenMenus] = useState<{ [key: string]: boolean }>({
    inventory: true,
    crm: true,
    accounting: false,
    hr: false,
  });

  const handleMenuToggle = (menu: string) => {
    setOpenMenus(prev => ({
      ...prev,
      [menu]: !prev[menu],
    }));
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') {
      return true;
    }
    if (path !== '/' && location.pathname.startsWith(path)) {
      return true;
    }
    return false;
  };

  const navItems: NavItem[] = [
    {
      title: 'Dashboard',
      path: '/',
      icon: <DashboardIcon />,
    },
    {
      title: 'Inventory',
      icon: <InventoryIcon />,
      children: [
        {
          title: 'Products',
          path: '/inventory/products',
          icon: <ShoppingCartIcon />,
        },
        {
          title: 'Categories',
          path: '/inventory/categories',
          icon: <CategoryIcon />,
        },
        {
          title: 'Warehouses',
          path: '/inventory/warehouses',
          icon: <WarehouseIcon />,
        },
        {
          title: 'Stock Levels',
          path: '/inventory/stock',
          icon: <AssessmentIcon />,
        },
      ],
    },
    {
      title: 'CRM',
      icon: <PeopleIcon />,
      children: [
        {
          title: 'Contacts',
          path: '/crm/contacts',
          icon: <ContactPhoneIcon />,
        },
        {
          title: 'Leads',
          path: '/crm/leads',
          icon: <PersonIcon />,
        },
        {
          title: 'Sales Pipeline',
          path: '/crm/pipeline',
          icon: <LeaderboardIcon />,
        },
      ],
    },
    {
      title: 'Accounting',
      icon: <AccountBalanceIcon />,
      children: [
        {
          title: 'Invoices',
          path: '/accounting/invoices',
          icon: <ReceiptIcon />,
        },
        {
          title: 'Expenses',
          path: '/accounting/expenses',
          icon: <AttachMoneyIcon />,
        },
        {
          title: 'Payments',
          path: '/accounting/payments',
          icon: <PaymentsIcon />,
        },
      ],
    },
    {
      title: 'HR',
      icon: <WorkIcon />,
      children: [
        {
          title: 'Employees',
          path: '/hr/employees',
          icon: <PeopleIcon />,
        },
        {
          title: 'Attendance',
          path: '/hr/attendance',
          icon: <AccessTimeIcon />,
        },
      ],
    },
  ];

  const renderNavItems = (items: NavItem[]) => {
    return items.map((item) => {
      if (item.children) {
        return (
          <React.Fragment key={item.title}>
            <ListItem disablePadding>
              <ListItemButton onClick={() => handleMenuToggle(item.title.toLowerCase())}>
                <ListItemIcon sx={{ color: theme.palette.primary.main }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.title} />
                {openMenus[item.title.toLowerCase()] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
            </ListItem>
            <Collapse in={openMenus[item.title.toLowerCase()]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.children.map((child) => (
                  <ListItem key={child.title} disablePadding>
                    <ListItemButton
                      sx={{ pl: 4 }}
                      selected={isActive(child.path || '')}
                      onClick={() => handleNavigation(child.path || '')}
                    >
                      <ListItemIcon sx={{ color: isActive(child.path || '') ? theme.palette.primary.main : 'inherit' }}>
                        {child.icon}
                      </ListItemIcon>
                      <ListItemText primary={child.title} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        );
      } else {
        return (
          <ListItem key={item.title} disablePadding>
            <ListItemButton
              selected={isActive(item.path || '')}
              onClick={() => handleNavigation(item.path || '')}
            >
              <ListItemIcon sx={{ color: isActive(item.path || '') ? theme.palette.primary.main : 'inherit' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.title} />
            </ListItemButton>
          </ListItem>
        );
      }
    });
  };

  const drawer = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', color: theme.palette.primary.main }}>
          OdooLike ERP
        </Typography>
        {isMobile && (
          <IconButton onClick={onClose} edge="end">
            <MenuOpenIcon />
          </IconButton>
        )}
      </Box>
      <Divider />
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        <List>{renderNavItems(navItems)}</List>
      </Box>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Typography variant="caption" color="text.secondary">
          © 2023 OdooLike ERP
        </Typography>
      </Box>
    </Box>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
    >
      {/* Mobile drawer */}
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={open}
          onClose={onClose}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
      ) : (
        /* Desktop drawer */
        <Drawer
          variant="permanent"
          open
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
      )}
    </Box>
  );
};

export default Sidebar;
