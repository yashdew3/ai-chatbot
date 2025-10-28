import React, { createContext, useContext, useState, useEffect } from 'react';
import apiClient from '../services/api'; // <--- IMPORT THE API CLIENT

interface AuthContextType {
  isAuthenticated: boolean;
  user: { email: string } | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<{ email: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Auto-authenticate for free tier (no database required)
    setIsAuthenticated(true);
    setUser({ email: 'admin@chatbot.local' });
    setLoading(false);
  }, []);

  // Auto-login for free tier (no authentication required)
  const login = async (email: string, password: string): Promise<boolean> => {
    setIsAuthenticated(true);
    setUser({ email: email || 'admin@chatbot.local' });
    return true;
  };  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    setIsAuthenticated(false);
    setUser(null);
  };

  const value = {
    isAuthenticated,
    user,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};