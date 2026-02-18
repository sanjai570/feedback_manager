import React, { createContext, useState, useContext, useEffect } from 'react';
import { userApi } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage for persisted user
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        try {
            // 1. Get Token
            const response = await userApi.login(email, password);
            const tokens = response.data; // { access, refresh }

            // Temporary storage to allow getMe to work
            const tempUser = { ...tokens };
            localStorage.setItem('user', JSON.stringify(tempUser));

            // 2. Get User Profile
            const meResponse = await userApi.getMe();
            const userData = meResponse.data;

            // Merge tokens and user data
            const fullUser = { ...userData, ...tokens };

            setUser(fullUser);
            localStorage.setItem('user', JSON.stringify(fullUser));
            return fullUser;
        } catch (error) {
            localStorage.removeItem('user'); // Clean up if failed
            throw error;
        }
    };

    const signup = async (userData) => {
        try {
            const response = await userApi.create(userData);
            // Signup usually returns user data, but not token?
            // If we want auto-login, we need to call login after signup.
            // For now, let's just return the new user and let component handle login redirect.
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
