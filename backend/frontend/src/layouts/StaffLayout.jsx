import React from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Box, Calendar, LogOut, GraduationCap, LayoutDashboard } from 'lucide-react';

const StaffLayout = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/landing');
    };

    return (
        <div className="app-container">
            <aside className="sidebar">
                <div className="logo-container">
                    <GraduationCap size={28} style={{ color: 'var(--primary)', marginRight: '0.5rem' }} />
                    <span className="logo-text">Campus Staff</span>
                </div>

                <ul className="nav-links">
                    <li>
                        <NavLink to="/staff/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                            <LayoutDashboard size={18} /> Dashboard
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/staff/resources" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                            <Box size={18} /> Resources
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/staff/bookings" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                            <Calendar size={18} /> Bookings
                        </NavLink>
                    </li>
                </ul>

                <div className="user-profile">
                    <div className="user-card mb-4">
                        <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'var(--primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px', fontWeight: 'bold' }}>
                            {user?.name?.charAt(0) || 'S'}
                        </div>
                        <div style={{ flex: 1, overflow: 'hidden' }}>
                            <p style={{ fontSize: '0.875rem', fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{user?.name}</p>
                            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Staff Member</p>
                        </div>
                    </div>
                    <button onClick={handleLogout} className="logout-btn">
                        <LogOut size={18} /> Logout
                    </button>
                </div>
            </aside>

            <main className="main-content">
                <div className="content-wrapper">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default StaffLayout;
