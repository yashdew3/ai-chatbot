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
    const token = localStorage.getItem('authToken');
    const userEmail = localStorage.getItem('userEmail');
    if (token && userEmail) {
      setIsAuthenticated(true);
      setUser({ email: userEmail });
    }
    setLoading(false);
  }, []);

  // --- START OF MODIFIED CODE ---
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await apiClient.post('/login', { email, password });
      
      if (response.status === 200 && response.data.token) {
        const { token } = response.data;
        localStorage.setItem('authToken', token);
        localStorage.setItem('userEmail', email);
        setIsAuthenticated(true);
        setUser({ email });
        return true;
      }
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
    return false;
  };
  // --- END OF MODIFIED CODE ---

  const logout = () => {
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