import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { ThemeToggle } from '../ui/theme-toggle';
import { 
  FaRobot, 
  FaTachometerAlt, 
  FaDatabase, 
  FaCog, 
  FaSignOutAlt,
  FaUser
} from 'react-icons/fa';

const Sidebar: React.FC = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    {
      path: '/admin/dashboard',
      icon: FaTachometerAlt,
      label: 'Dashboard',
    },
    {
      path: '/admin/knowledge-base',
      icon: FaDatabase,
      label: 'Knowledge Base',
    },
    {
      path: '/admin/settings',
      icon: FaCog,
      label: 'Settings',
    },
  ];

  return (
    <div className="w-64 bg-card/80 border-r border-border backdrop-blur-xl">
      <div className="p-6">
        {/* Logo */}
        <div className="flex items-center space-x-3 mb-8">
          <div className="p-2 rounded-lg bg-primary/10 border border-primary/20">
            <FaRobot className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">AI Assistant</h1>
            <p className="text-xs text-muted-foreground">Admin Panel</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-lg transition-smooth hover-lift ${
                  isActive
                    ? 'bg-primary/10 text-primary border border-primary/20 shadow-lg'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                }`
              }
            >
              <item.icon className="h-5 w-5" />
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      {/* User section at bottom */}
      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-border">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-secondary">
              <FaUser className="h-4 w-4 text-secondary-foreground" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">
                {user?.email}
              </p>
              <p className="text-xs text-muted-foreground">Administrator</p>
            </div>
          </div>
          <ThemeToggle />
        </div>
        <Button
          onClick={handleLogout}
          variant="outline"
          size="sm"
          className="w-full hover:bg-destructive/10 hover:text-destructive hover:border-destructive/50"
        >
          <FaSignOutAlt className="h-4 w-4 mr-2" />
          Sign Out
        </Button>
      </div>
    </div>
  );
};

export default Sidebar;