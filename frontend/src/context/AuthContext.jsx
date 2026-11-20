import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('studentpulse_token'));
  const [loading, setLoading] = useState(true);
  const [systemInfo, setSystemInfo] = useState(null);

  // Fetch system health & current user on load
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Fetch system info (AI status, health)
        const healthRes = await api.get('/health');
        setSystemInfo(healthRes.data);
      } catch (err) {
        console.warn('System health check error:', err);
      }

      if (token) {
        try {
          const userRes = await api.get('/auth/me');
          setUser(userRes.data);
        } catch (err) {
          console.error('Failed to load authenticated user profile:', err);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, [token]);

  const login = async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    const { access_token, user: userData } = response.data;
    localStorage.setItem('studentpulse_token', access_token);
    setToken(access_token);
    setUser(userData);
    return response.data;
  };

  const register = async (userData) => {
    const response = await api.post('/auth/register', userData);
    const { access_token, user: newUser } = response.data;
    localStorage.setItem('studentpulse_token', access_token);
    setToken(access_token);
    setUser(newUser);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('studentpulse_token');
    localStorage.removeItem('studentpulse_user');
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const res = await api.get('/auth/me');
      setUser(res.data);
    } catch (err) {
      console.error('Failed to refresh user:', err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        systemInfo,
        login,
        register,
        logout,
        refreshUser,
        isAuthenticated: !!token && !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
