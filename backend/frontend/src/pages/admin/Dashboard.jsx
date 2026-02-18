import React, { useEffect, useState } from 'react';
import { Users, Box, Calendar, CheckCircle, Clock } from 'lucide-react';
import { userApi, resourceApi, bookingApi } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className="stat-card">
        <div className="flex items-center gap-2 mb-4">
            <div style={{
                padding: '8px',
                borderRadius: '8px',
                background: `var(--${color}-bg)`,
                color: `var(--${color})`,
                display: 'inline-flex'
            }}>
                <Icon size={20} strokeWidth={2.5} />
            </div>
            <span className="stat-label" style={{ marginBottom: 0 }}>{label}</span>
        </div>
        <div className="stat-value">{value}</div>
    </div>
);

const AdminDashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState({
        users: 0,
        resources: 0,
        bookings: 0,
        pending: 0,
        approved: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const results = await Promise.all([
                    resourceApi.getAll(),
                    bookingApi.getAll(),
                    userApi.getAll()
                ]);

                const resources = results[0].data || [];
                const bookings = results[1].data || [];
                const usersData = results[2].data || [];

                setStats({
                    users: usersData.length,
                    resources: resources.length,
                    bookings: bookings.length,
                    pending: bookings.filter(b => b.status === 'PENDING').length,
                    approved: bookings.filter(b => b.status === 'APPROVED').length
                });
            } catch (error) {
                console.error("Failed to fetch dashboard stats", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchStats();
        }
    }, [user]);

    if (loading) return <div className="p-4 text-center text-muted">Loading dashboard...</div>;

    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    return (
        <div>
            <div className="page-header">
                <div>
                    <h1 className="page-title">Dashboard</h1>
                    <p className="page-subtitle">{date} • Welcome back, {user?.name}</p>
                </div>
            </div>

            <div className="dashboard-grid">
                <StatCard
                    icon={Users}
                    label="Total Users"
                    value={stats.users}
                    color="primary"
                />
                <StatCard
                    icon={Box}
                    label="Total Resources"
                    value={stats.resources}
                    color="primary"
                />
                <StatCard
                    icon={Calendar}
                    label="Total Bookings"
                    value={stats.bookings}
                    color="primary"
                />
                <StatCard
                    icon={Clock}
                    label="Pending Bookings"
                    value={stats.pending}
                    color="warning"
                />
                <StatCard
                    icon={CheckCircle}
                    label="Approved Bookings"
                    value={stats.approved}
                    color="success"
                />
            </div>
        </div>
    );
};

export default AdminDashboard;
